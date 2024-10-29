# simply loop through all production folders while submitting with proper project names.
# do the bespokefit ones first.
topdir=$(pwd)
for i in {1..5}; do
    echo "REPLICATE $i"
    cd ./bespokefit_benchmarks_$i
    echo "Submitting Bespoke.."
    for target in *; do
        cd $target
        echo $target
        asap-alchemy submit -c public -p benchmark_${target}_bespoke_$i
        cd ../
    done

    # then do the non-bespoke, default ones.
    cd ../
    cd ./default_benchmarks_$i
    echo "Submitting Default.."
    for target in *; do
        cd $target
        echo $target
        asap-alchemy submit -c public -p benchmark_${target}_default_$i
        cd ../
    done
    echo "Done"

    cd $topdir
done