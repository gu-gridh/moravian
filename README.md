# Moravian Lives Sweden

Django backend for the Swedish version of Moravian Lives.

It uses the gridh-pages app to create simple static pages.

# Run in Container
Install `podman-compose` if you haven't already. It works best with a .env file in the moravian folder with the same values for DB_LOCAL_NAME, DB_LOCAL_USER, 
DB_LOCAL_PASS, HOST, PORT, DJANGO_SETTINGS_MODULE as in podman-compose.yml. Then run
```
podman-compose up --build
```
in the same folder as the podman-compose file. Wait for the containers to build (it also loads sample data so it might take a while).
Go to `localhost:8000` to see the running django instance.

The container reacts to changes in the repository as the project folder is loaded as a volume.

## Updating CSS
Assuming you have a current node version installed (repo is tested with node version 22), run 
`npm install` in /moravian (where package.json is) if you haven't already. 

Run `npx gulp watch` every time you run the containers and change css files if needed. It should update automatically, delete your browser cache otherwise.

# Create sample data
In the productive system, run 
```
conda activate moravian
./manage.py shell --settings=moravian.settings.production
>>> from trxnviewer.utils import dump_related_sample
>>> dump_related_sample()
```
which creates the sample data in `trxnviewer/fixtures`.
