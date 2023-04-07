#!/usr/bin/sh

#> sp_metrics.out;
echo "mode Nc rep time_per_step tot_time numb_try numb_succ auto_time_sec Emean Ese count conv_crit" #> ../../../sp_metrics.out;

for i in */*/*/; do 
  cd $i;
#  pwd;
  # get simulation param info
  mode=$(echo $i | cut -d'/' -f1)
  Nc=$(echo $i | cut -d'/' -f2)
  rep=$(echo $i | cut -d'/' -f3)

  # get recorded info in result.out (acceptance rate, time, etc.)
  res_file=$(cat result.out);
  tot_time=$(echo $res_file | cut -d' ' -f2);
  tperstep=$(echo $res_file | cut -d' ' -f4);
  printf -v tperstep_f "%.12f" "$tperstep"
  try=$(echo "scale=0; $tot_time/$tperstep_f" | bc -l);
  succ=$(echo $res_file | cut -d' ' -f6);

  # run autocor.py and collect autocorrelation time and other metrics
  ../../../autocor.py;
  auto_file=$(cat autocorr_result.out);
  auto_time=$(echo $auto_file | cut -d' ' -f5);
  Emean=$(echo $auto_file | cut -d' ' -f15);
  count=$(echo $auto_file | cut -d' ' -f20);
  Ese=$(echo $auto_file | cut -d' ' -f25);
  conv=$(echo $auto_file | cut -d' ' -f30);

  # print to file
  echo $mode $Nc $rep $tperstep $tot_time $try $succ $auto_time $Emean $Ese $count $conv #>> ../../../sp_metrics.out;

  cd ../../../;
#  break;
done;
