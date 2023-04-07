#!/bin/bash

# DEFAULTS:
# format=( Nc Nb T rho eps sigma rc multip MCm EQm pfq errorCh readIn rangel rangeh binSize flatTol Nmax Pcs Per Pdbl eps_bond rnot_bond delrmax_bond )
defaults=( 100 100 5.0 0.15 1.0 1.0 2.5 1.0 1000 100 100 0 0 -30000.0 -15000.0 10.0 0.2 40 0.6 0.3 0.05 2000.0 1.0 1.0 2.5 )

array_format="Nc" # Format of params array
array=( 30000 90000 200000 520000 )
#100.0:0.3:-30000.0:-27600.0 100.0:0.3:-28200.00:-27000.00 100.0:0.3:-27600.00:-26400.00 100.0:0.3:-27000.00:-25800.00 100.0:0.3:-26400.00:-25200.00 100.0:0.3:-25800.00:-24600.00 100.0:0.3:-25200.00:-24000.00 100.0:0.3:-24600.00:-23400.00 100.0:0.3:-24000.00:-22800.00 100.0:0.3:-23400.00:-22200.00 100.0:0.3:-22800.00:-21600.00 100.0:0.3:-22200.00:-21000.00 100.0:0.3:-21600.00:-20400.00 100.0:0.3:-21000.00:-19800.00 100.0:0.3:-20400.00:-19200.00 100.0:0.3:-19800.00:-18600.00 100.0:0.3:-19200.00:-18000.00 100.0:0.3:-18600.00:-17400.00 100.0:0.3:-18000.00:-16800.00 100.0:0.3:-17400.00:-15000.00
typeSim=( ser\ LJ\ pol par\ LJ\ pol ) # The type of simulations and command line options for C++ exec. There needs to be one array with the name $typeSim[i]_sim_time format for each i in typeSim
def2=72:00:00
def3=1000:100
par_LJ_pol_sim_time=( $def2 $def2 $def2 $def2 $def2 ) # parallel job time limit (d for default)

ser_LJ_pol_sim_time=( $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 $def2 ) # serial job time limt (d for default)
ser_LJ_pol_MCm=( $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 $def3 )
par_LJ_pol_MCm=( $def3 $def3 $def3 $def3 $def3 )
Rep=( 1 )
dir_name="largerNcSweep"

# the following determines what input type and which column to change in params.dat
IFS=':' read -ra param_type <<< "$array_format"
ITER=0
for i in "${param_type[@]}"
do
	if [ $i == Nc ]
	then
		param_i[$ITER]=0
	fi
	if [ $i == Nb ]
	then
		param_i[$ITER]=1
	fi
	if [ $i == T ]
	then
		param_i[$ITER]=2
	fi
	if [ $i == rho ]
	then
		param_i[$ITER]=3
	fi
	if [ $i == rc ]
	then
		param_i[$ITER]=6
	fi
	if [ $i == MCm ]
	then
		param_i[$ITER]=8
	fi
	if [ $i == EQm ]
	then
		param_i[$ITER]=9
	fi
	if [ $i == pfq ]
	then
		param_i[$ITER]=10
	fi
	if [ $i == errorCh ]
	then
		param_i[$ITER]=11
	fi
	if [ $i == readIn ]
	then
		param_i[$ITER]=12
	fi
	if [ $i == rangel ]
	then
		param_i[$ITER]=13
	fi
	if [ $i == rangeh ]
	then
		param_i[$ITER]=14
	fi
	if [ $i == binSize ]
	then
		param_i[$ITER]=15
	fi
	if [ $i == flatTol ]
	then
		param_i[$ITER]=16
	fi
	if [ $i == Nmax ]
	then
		param_i[$ITER]=17
	fi
	if [ $i == Pcs ]
	then
		param_i[$ITER]=18
	fi
	if [ $i == Per ]
	then
		param_i[$ITER]=19
	fi
	if [ $i == Pdbl ]
	then
		param_i[$ITER]=20
	fi
	ITER=$ITER+1
done

# making the directory using dir_name
mkdir $dir_name
cd $dir_name
if [ -d "cu" ]
then
	exit 1
fi
cp ../../bin/rel.out .
cp ../../tools/autocorr.py .
cp ../../scripts/jobmak.sh .
cp ../params.dat .
me="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
cp ../$me .
mapfile < params.dat
IFS=' ' read -ra ind <<< "${MAPFILE[0]}"
param_count=0
for param in "${defaults[@]}"
do
	ind[$param_count]=$param
	param_count=$param_count+1
done
MAPFILE[0]=""
for jk in "${ind[@]}"
do
	MAPFILE[0]+="$jk "	
done
printf "%s\n" "${MAPFILE[@]}" > params.dat
for ij in "${typeSim[@]}"
do
	ij_u="${ij// /_}"
	mkdir $ij_u
	cd $ij_u
	cp ../rel.out .
	cp ../autocorr.py .
	cp ../jobmak.sh .
	cp ../params.dat .
	ITER=0
	for i in "${array[@]}"
	do
		mkdir $i
		cd $i
		cp ../rel.out .
		cp ../autocorr.py .
		cp ../jobmak.sh .
		cp ../params.dat .
		
#reading params.dat
		IFS=':' read -ra N <<< "$i"
		mapfile < params.dat
		IFS=' ' read -ra ind <<< "${MAPFILE[0]}"
#substituting information in array!
		for PARAM in "${!param_type[@]}"
		do
			ind[${param_i[$PARAM]}]=${N[$PARAM]}
		done
#changing MCm, EQm and pfq according to values in corresponding arrays
		MCmEQm_str=${ij_u}_MCm[$ITER]
		MCmEQm_num=${!MCmEQm_str}
		if [ $MCmEQm_num != d ]
		then
			IFS=':' read -ra MCEQ <<< "${!MCmEQm_str}"
			ind[8]=${MCEQ[0]}
			ind[9]=${MCEQ[1]}
			ind[10]=${MCEQ[1]}
		fi
#Filling back into MAPFILE and printing to params.dat
		MAPFILE[0]=""
		for j in "${ind[@]}"
		do
			MAPFILE[0]+="$j "
		done
		printf "%s\n" "${MAPFILE[@]}" > params.dat
		
#changing jobmak.sh
		IFS=' ' read -ra ij_ind <<< "$ij"	
		sim_time_elem=${ij_u}_sim_time[$ITER]
		sim_time=${!sim_time_elem}
		options="${ij}"
		mapfile < jobmak.sh
		if [ $sim_time != d ]
		then
			IFS='=' read -ra ind <<< "${MAPFILE[2]}"
			ind[1]=$sim_time
			MAPFILE[2]=""
			MAPFILE[2]+="${ind[0]}"
			MAPFILE[2]+="="
			MAPFILE[2]+="${ind[1]}"
		fi
		if [ ${ij_ind[0]} != ser ] && [ ${ij_ind[0]} != serwl ]
		then
			MAPFILE=( "${MAPFILE[@]:0:5}" "#SBATCH --gres=gpu:1 #always use 4 for every node" "${MAPFILE[@]:5}" )
			MAPFILE=( "${MAPFILE[@]:0:6}" "#SBATCH -C 'rhel7&pascal' #features syntax (use quotes): -C 'a&b&c&d'
" "${MAPFILE[@]:7}" )
			MAPFILE=( "${MAPFILE[@]:0:7}" "#SBATCH --mem-per-cpu=130000M # memory per CPU core
" "${MAPFILE[@]:8}" )
		fi
		MAPFILE[${#MAPFILE[@]}-1]="./rel.out $options"
		printf "%s\n" "${MAPFILE[@]}" > jobmak.sh

		for jk in "${Rep[@]}"
		do
			mkdir $jk
			cd $jk
			rm slurm-*
			cp ../rel.out .
			cp ../autocorr.py .
			#cp lng_init.out lng.out
			#cp lng.out lng_init17.out
			#cp config_final.out config_init17.out
			cp ../jobmak.sh .
			cp ../params.dat .	
			#cp ../config_final.out .
			#cp config_final.out config_init.out
			pwd
	       		sbatch jobmak.sh
			cd ..
		done
		ITER=$ITER+1
		cd ..
	done
	cd ..
done
