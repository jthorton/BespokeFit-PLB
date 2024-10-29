# simply loop through all production folders while submitting with proper project names.
# do the bespokefit ones first.
topdir=$(pwd)
for i in {2..5}; do
    echo "REPLICATE $i"
    cd ./bespokefit_benchmarks_$i
    echo "Gathering Bespoke.."
    for target in *; do
        cd $target
        echo $target
        asap-alchemy gather
        cd ../
    done

    # then do the non-bespoke, default ones.
    cd ../
    cd ./default_benchmarks_$i
    echo "Gathering Default.."
    for target in *; do
        cd $target
        echo $target
        asap-alchemy gather
        cd ../
    done
    echo "Done"

    cd $topdir
done