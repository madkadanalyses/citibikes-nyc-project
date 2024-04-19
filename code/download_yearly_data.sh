set -e

declare -a arr=("2019" "2022")

URL_PREFIX="https://s3.amazonaws.com/tripdata"

#https://s3.amazonaws.com/tripdata/2017-citibike-tripdata.zip

for YEAR in ${arr[@]}; do

  URL="${URL_PREFIX}/${YEAR}-citibike-tripdata.zip"

  LOCAL_PREFIX="data/raw/${YEAR}"
  LOCAL_FILE="citibike_tripdata_${YEAR}.zip"
  LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

  echo "downloading ${URL} to ${LOCAL_PATH}"
  mkdir -p ${LOCAL_PREFIX}
  wget ${URL} -O ${LOCAL_PATH}

  echo "unzipping"
  cd ${LOCAL_PREFIX}
  unzip ${LOCAL_FILE}

done