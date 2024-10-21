# simply loop through all production folders while submitting with proper project names.
# do the bespokefit ones first.
cd ./bespokefit_benchmarks
echo "Submitting Bespoke.."
for target in *; do
    cd $target
    echo $target
    asap-alchemy submit -c public -p benchmark_${target}_bespoke
    cd ../
done

# then do the non-bespoke, default ones.
cd ../
cd ./default_benchmarks
echo "Submitting Default.."
for target in *; do
    cd $target
    echo $target
    asap-alchemy submit -c public -p benchmark_${target}_default
    cd ../
done
echo "Done"