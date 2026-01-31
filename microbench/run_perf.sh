#!/bin/bash

#This script will run multiple data structure/allocator configurations and merge and average of perf results into a single file

script_dir=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
alloc_dir=$script_dir/lib/allocators

if [ ! -d "$alloc_dir" ]; then 
  ./build.sh
fi

d=$(date +%F-%H:%M:%S)
mkdir -p perf_results/${d}
pushd perf_results/${d}

allocators="mimalloc jemalloc:numa"
runs=1
update_percs="100"
trackers="2geibr 2geibr_df debra debra_df he he_df ibr_hp ibr_hp_df ibr_rcu ibr_rcu_df nbr nbr_df nbrplus nbrplus_df qsbr qsbr_df token4 wfe wfe_df"
#different data structures will require different sizes"
rideables_sizes="guerraoui_ext_bst_ticket:200000 brown_ext_abtree_lf:200000 hm_hashtable:200000 hmlist:2000"

for rideable_size in $(echo "$rideables_sizes"); do
  for tracker in $(echo "$trackers"); do
    for update_perc in $(echo "$update_percs"); do
      for allocator_wnuma in $(echo "$allocators"); do
        rideable=$(echo $rideable_size | cut -d: -f1)
        size=$(echo $rideable_size | cut -d: -f2)
        update_half=$(python -c "print(int($update_perc/2))")
        #decide whether to use numactl or not
        allocator=$(echo $allocator_wnuma | cut -d: -f1)
        numa_suffix=$(echo $allocator_wnuma | cut -d: -f2)
        if [[ "$numa_suffix" = numa ]]; then
          use_numa=true
          numa_suffix="numactl -i all"
          numa_name="_numa"
        else
          use_numa=false
          numa_suffix=""
          numa_name=""
        fi
        for a in $(seq $runs); do
          perf_file=perf_${allocator}${numa_name}_${rideable}:${size}_${tracker}_${update_perc}u_${a}.data
          NO_DESTRUCT=1 LD_PRELOAD=${alloc_dir}/lib${allocator}.so \
          $numa_suffix perf record -o $perf_file \
          ${script_dir}/bin/ubench_${rideable}.alloc_new.reclaim_${tracker}.pool_none.out \
          -nwork $(nproc) -nprefill $(nproc) -i $update_half -d $update_half -rq 0 -rqsize 1 -k \
          $size -nrq 0 -t 5000 2>&1
          perf report -i $perf_file --stdio > ${perf_file}.txt
          rm $perf_file
        done
      done
    done
  done
done

for allocator_wnuma in $(echo "$allocators"); do
  allocator=$(echo $allocator_wnuma | cut -d: -f1)
  numa_suffix=$(echo $allocator_wnuma | cut -d: -f2)
  if [[ "$numa_suffix" = numa ]]; then numa_name="_numa"; else numa_name=""; fi
  python3 ${script_dir}/merge_perf_txt.py perf_${allocator}${numa_name}_*.data.txt | tee perf_merge_${allocator}${numa_name}.merge.txt
  python3 ${script_dir}/perf_plot.py perf_${allocator}${numa_name}_*.data.txt
  mv perf_plot.png perf_${allocator}${numa_name}.png
  mv perf_plot.pdf perf_${allocator}${numa_name}.pdf
  mv allocator_data.csv ${allocator}${numa_name}_data.csv
done

popd
