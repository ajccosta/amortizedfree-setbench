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

allocators="mimalloc jemalloc"
runs=1
update_percs="100"
trackers="2geibr debra he ibr_hp ibr_rcu nbr nbrplus qsbr token4 wfe"
#different data structures will require different sizes"
rideables_sizes="guerraoui_ext_bst_ticket:200000 brown_ext_abtree_lf:200000 hm_hashtable:200000 hmlist:2000"

for rideable_size in $(echo "$rideables_sizes"); do
  for tracker in $(echo "$trackers"); do
    for update_perc in $(echo "$update_percs"); do
      for allocator in $(echo "$allocators"); do 
        for use_numa in false true; do
          rideable=$(echo $rideable_size | cut -d: -f1)
          size=$(echo $rideable_size | cut -d: -f2)
          update_half=$(python -c "print(int($update_perc/2))")
          #decide whether to use numactl or not
          if [[ "$use_numa" = true ]]; then numa_suffix="numactl -i all"; else numa_suffix=""; fi
          if [[ "$use_numa" = true ]]; then numa_name="_numa"; else numa_name="_nonuma"; fi
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
done

for allocator in $(echo "$allocators"); do 
  for numa_name in "_numa" "_nonuma"; do
    python3 ${script_dir}/merge_perf_txt.py perf_${allocator}${numa_name}_*.data.txt | tee perf_merge_${allocator}${numa_name}.merge.txt
    python3 ${script_dir}/perf_plot.py perf_${allocator}${numa_name}_*.data.txt
    mv perf_plot.png perf_${allocator}${numa_name}.png
    mv perf_plot.pdf perf_${allocator}${numa_name}.pdf
  done
done

popd