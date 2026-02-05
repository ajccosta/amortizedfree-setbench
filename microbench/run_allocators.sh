#!/bin/bash
alloc_dir=lib/allocators

if [ ! -d "$alloc_dir" ]; then 
  ./build.sh
fi

#:numa means the allocator will be run with numactl -i all
#:df means that it will utilize the deferred/amortized freeing technique
# We chose which allocator uses what based on experimental results.
# It is highly machine dependent, and some allocators have no clear
# best configuration, as the best changes from data structure to data structure.
allocators="deqalloc mimalloc jemalloc:numa:df snmalloc hoard:numa tcmalloc::df tbbmalloc::df lockfree:numa:df rpmalloc::df"
runs=3
update_percs="1 5 50 90 100"
trackers="2geibr debra he ibr_hp ibr_rcu nbr nbrplus qsbr wfe"
#different data structures will require different sizes"
#small-sized data structures
rideables_sizes="guerraoui_ext_bst_ticket:5000 brown_ext_abtree_lf:5000 hm_hashtable:5000 hmlist:500"
#medium-sized data structures
rideables_sizes+=" guerraoui_ext_bst_ticket:200000 brown_ext_abtree_lf:200000 hm_hashtable:200000 hmlist:2000"
#medium-large-sized data structures
rideables_sizes+=" guerraoui_ext_bst_ticket:20000000 brown_ext_abtree_lf:20000000 hm_hashtable:2000000 hmlist:10000"
#large-sized data structures
rideables_sizes+=" guerraoui_ext_bst_ticket:200000000 brown_ext_abtree_lf:200000000 hm_hashtable:20000000 hmlist:10000"

fmt="%-12s %-10s %-10s %-25s %-10s %-6s %s"
printf "$fmt\n" "allocator" "update%" "scheme" "ds" "key_size" "numa" "results"
for rideable_size in $(echo "$rideables_sizes"); do
  for tracker in $(echo "$trackers"); do
    for update_perc in $(echo "$update_percs"); do
      for allocator_wnuma in $(echo "$allocators"); do
        rideable=$(echo $rideable_size | cut -d: -f1)
        size=$(echo $rideable_size | cut -d: -f2)
        update_half=$(python -c "print(int($update_perc/2))")
        #remove :numa from allocator
        allocator=$(echo $allocator_wnuma | cut -d: -f1)
        numa_suffix=$(echo $allocator_wnuma | cut -d: -f2)
        if [[ "$numa_suffix" = numa ]]; then
          use_numa=true
          numa_suffix="numactl -i all"
        else
          use_numa=false
          numa_suffix=""
        fi
        df_suffix=$(echo $allocator_wnuma | cut -d: -f3)
        if [[ "$df_suffix" = df ]]; then
          df_suffix="_df"
        else
          df_suffix=""
        fi
        if [[ "${rideable}" == "brown_ext_abtree_lf" && "${tracker}" == *"nbr"* ]]; then
          #brown_ext_abtree_lf with nbr or nbr_plus segfaults
          continue
        fi
        #decide whether to use numactl or not
        printf "$fmt" "$allocator" "$update_perc" "${tracker}${df_suffix}" "$rideable" "$size" "$use_numa" "[ "
        tp_avg=0
        memusage_avg=0
        raw=""
        for a in $(seq $runs); do
          NO_DESTRUCT=1 res=$(LD_PRELOAD=${alloc_dir}/lib${allocator}.so \
          /usr/bin/time -f "%M KiloBytes /usr/bin/time output" $numa_suffix \
          ./bin/ubench_${rideable}.alloc_new.reclaim_${tracker}${df_suffix}.pool_none.out \
          -nwork $(nproc) -nprefill $(nproc) -i $update_half -d $update_half -rq 0 -rqsize 1 -k \
          $size -nrq 0 -t 5000 2>&1)
          tp=$(echo -e "$res" | grep "total throughput" | tr -s ' ' | cut -d' ' -f4)
          tp_avg=$(python -c "print($tp_avg+($tp/$runs))")
          memusage=$(echo -e "$res" | grep "KiloBytes /usr/bin/time output" | cut -d' ' -f1)
          memusage_avg=$(python -c "print(int($memusage_avg+($memusage/$runs)))")
          raw="$raw $res"
          printf "$tp "
        done
        printf "] $tp_avg, ${memusage_avg} KB\n"
      done
    done
  done
done
