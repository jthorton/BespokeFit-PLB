# simply loop through all production folders while gathering.
# do the bespokefit ones first.
cd ./bespokefit_benchmarks
echo "Gathering Bespoke.."
for target in *; do
    cd $target
    echo $target
    asap-alchemy gather
    cd ../
done

# then do the non-bespoke, default ones.
cd ../
cd ./default_benchmarks
echo "Gathering Default.."
for target in *; do
    cd $target
    echo $target
    asap-alchemy gather
    cd ../
done
echo "Done"