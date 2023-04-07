#!/bin/bash

array=( 100 200 550 1100 2000 5100 9000 )
mkdir Ncsweep3
cd Ncsweep3
if [ -d "cu" ]
then
	exit 1
fi
cp ../../bin/rel.out .
cp ../../tools/autocorr.py .
cp ../../scripts/jobmak.sh .
cp ../params.dat .
vim params.dat
for ij in par
do
	mkdir $ij
	cd $ij
	cp ../rel.out .
	cp ../autocorr.py .
	cp ../jobmak.sh .
	cp ../params.dat .
	echo "change jobmak for $ij"
	vim jobmak.sh
	for i in "${array[@]}"
	do
		mkdir $i
		cd $i
		cp ../rel.out .
		cp ../autocorr.py .
		cp ../jobmak.sh .
		cp ../params.dat .

	#	IFS=':' read -ra N <<< "$i"
		mapfile < params.dat
		IFS=' ' read -ra ind <<< "${MAPFILE[0]}"
		ind[0]=$i
		MAPFILE[0]=""
		for j in "${ind[@]}"
		do
			MAPFILE[0]+="$j "
		done
		printf "%s\n" "${MAPFILE[@]}" > params.dat
		for jk in 1
		do
			mkdir $jk
			cd $jk
			rm -rf *
			cp ../rel.out .
			cp ../autocorr.py .
			cp ../jobmak.sh .
			cp ../params.dat .			
	       		sbatch jobmak.sh
			cd ..
		done
		cd ..
	done
	cd ..
done
