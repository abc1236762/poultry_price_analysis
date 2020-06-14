pushd frontend
yarn build
popd
pushd ..
python -m poultry_price_analysis
