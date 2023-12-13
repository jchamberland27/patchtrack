# utility script to build docker image
echo "Build and deploy patchtrack docker image..."

# clear out any previous versions
docker stop patchtrack
docker rm patchtrack

#set $1 to default port if not passed in
if [ -z "$1" ]
  then
    echo "No port argument supplied, using default port 5002"
    set -- "5002"
fi

# move dockerfile into place
cp Dockerfile ../src/
cd ../src

# build and run docker image on port passed into script
docker image build -t patchtrack .
docker run -d --name patchtrack -v patchtrack:/app/db -p $1:5002 patchtrack

#cleanup
rm Dockerfile

# dump out running containers
echo "Running containers after deployment:"
docker ps

echo "Done."