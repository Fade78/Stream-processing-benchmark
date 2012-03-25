#!/bin/bash

COMMONPATH=common
OUTPUTDIR=output
DATAFILE="$OUTPUTDIR/data.txt"
DATAGENERATOR="$COMMONPATH/datagenerator.py"
BENCHLIST=benchlist.conf

if [ ! -d "$OUTPUTDIR" ]
then
	echo "Creating output dir $OUTPUTDIR"
	if $(mkdir "$OUTPUTDIR")
	then
		echo "Creation successful"
	else
		echo "Problem while creating output dir"
		exit -2
	fi
fi

if [ $(df "$OUTPUTDIR" | tail -1 | perl -a -ne 'print((($F[3]>250*1024)?"":"n")."ok")') == "nok" ]
then
	echo "You must have at least 250MB of free space."
	exit -2
fi

if [ ! -f "$DATAFILE" ]
then
	echo "Missing data file."
	if [ -f "$DATAGENERATOR" ]
	then
		type python3 > /dev/null 2>&1
		if [ $? -eq 1 ]
		then
			echo "You need python3 to generate dataset"
			exit -2
		fi
		echo "Generating data file."
		python3 "$COMMONPATH/datagenerator.py" > "$DATAFILE"
	else
		echo "Can't access $DATAGENERATOR"
		exit -1
	fi
fi

if [ $(cat "$DATAFILE" | md5sum | cut -d' ' -f1) != 'd990cca71b2730c9b28a8dfebcd3c1de' ]
# Check with # lines for data file.
then
	echo "Warning: data file is not standard"
fi

echo "Data file stats"
md5sum "$DATAFILE"
wc "$DATAFILE"
ls -lh "$DATAFILE"

checkreport () {
	# If you check by hand, don't forget to strip # lines!
	SUM=$(cat "$1" | grep -v '^#' | md5sum | cut -d' ' -f1)
	SUMREF=$2
	if [ "$SUMREF" == "$SUM" ]
	then
		echo "Report is correct ($SUM)."
	else
		echo "Report is not correct (ref:$SUMREF vs $SUM)!"
	fi
}

rm -f "$OUTPUTDIR"/benchref_*

# Running script
cat "$BENCHLIST" | perl -ne 's/[ 	]+/ /g;print unless /^\s*(?:#|$)/' | while read LABEL CATEGORY INTERPRETER SCRIPTPATH
do
	type "$INTERPRETER" > /dev/null 2>&1
        if [ $? -eq 0 ]
        then
		if [ -r $SCRIPTPATH ]
		then
			STDOUT="$OUTPUTDIR/bench_$(basename $INTERPRETER)_$(basename $SCRIPTPATH)_$(basename $CATEGORY).out.txt"
			STDERR="$OUTPUTDIR/bench_$(basename $INTERPRETER)_$(basename $SCRIPTPATH)_$(basename $CATEGORY).err.txt"
			echo "Running $LABEL"
			time cat "$DATAFILE" | "$INTERPRETER" "$SCRIPTPATH" > "$STDOUT" 2> "$STDERR"
			REF="$OUTPUTDIR/benchref_$CATEGORY"
			if [ -r "$REF" ]
			then
				checkreport "$STDOUT" $(cat "$REF")
			else
				echo $(cat "$STDOUT" | grep -v '^#' | md5sum | cut -d' ' -f1) > "$REF"
			fi
		else
			echo "Can't read $SCRIPTPATH"
		fi
	else
		echo "Can't find $INTERPRETER"
	fi
done
