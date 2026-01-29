#!/bin/bash
alloc_dir=lib/allocators

if [ ! -d "$alloc_dir" ]; then 
  ./build.sh
fi

allocators="deqalloc mimalloc jemalloc"
runs=5
update_percs="0 5 50 90 100"
trackers="2geibr 2geibr_df debra debra_df he he_df ibr_hp ibr_hp_df ibr_rcu ibr_rcu_df nbr nbr_df nbrplus nbrplus_df qsbr qsbr_df token4 wfe wfe_df"
#different data structures will require different sizes"
rideables_sizes="guerraoui_ext_bst_ticket:5000 brown_ext_abtree_lf:5000 hm_hashtable:5000 hmlist:500"
#rideables_sizes="guerraoui_ext_bst_ticket:200000 brown_ext_abtree_lf:200000 hm_hashtable:200000 hmlist:2000"
#rideables_sizes="guerraoui_ext_bst_ticket:20000000 brown_ext_abtree_lf:20000000 hm_hashtable:20000000 hmlist:10000"

fmt="%-12s %-10s %-10s %-25s %-10s %-6s %s"
printf "$fmt\n" "allocator" "update%" "scheme" "ds" "key_size" "numa" "results"
for rideable_size in $(echo "$rideables_sizes"); do
  for tracker in $(echo "$trackers"); do
    for update_perc in $(echo "$update_percs"); do
      for allocator in $(echo "$allocators"); do 
        for use_numa in false true; do
          rideable=$(echo $rideable_size | cut -d: -f1)
          size=$(echo $rideable_size | cut -d: -f2)
          update_half=$(python -c "print(int($update_perc/2))")
          if [[ "${rideable}" == "brown_ext_abtree_lf" && "${tracker}" == *"nbr"* ]]; then
            #brown_ext_abtree_lf with nbr or nbr_plus segfaults
            continue
          fi
          #decide whether to use numactl or not
          if [[ "$use_numa" = true ]]; then numa_suffix="numactl -i all"; else numa_suffix=""; fi
          printf "$fmt" "$allocator" "$update_perc" "$tracker" "$rideable" "$size" "$use_numa" "[ "
          tp_avg=0
          memusage_avg=0
          raw=""
          for a in $(seq $runs); do
            res=$(LD_PRELOAD=${alloc_dir}/lib${allocator}.so \
            /usr/bin/time -f "%M KiloBytes /usr/bin/time output" $numa_suffix \
            ./bin/ubench_${rideable}.alloc_new.reclaim_${tracker}.pool_none.out \
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
done