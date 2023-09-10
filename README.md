# Token Authentication in DRF

```shell
[][][][][]     [][][][]     [][][][]
[]        []   []     []    []
[]        []   []  [] []    [][][][]
[]        []   []    []     []
[][][][][]     []     []    []
```


# Setup 🔧

- clone repo
```shell
git clone <link to repo>
```
- Go into the folder
```shell
cd :\\path\\to\\cloned_repo
```
- install pipenv
```shell
pip install pipenv
```
- activate pipenv
```shell
make shell
```
- install dependencies
```shell
make install
```
- Create a copy of `.env.example` and rename to `.env` then fill in the values

- Run Migrations with:
`make makemigrations`
`make migrate`

- Create admin user with:
> whilst in project directory

`make py-shell`

Then:
```shell
>>> from authme.models import CustomUser

>>> CustomUser.objects.create_user(email="youremail@example.com",username="johnDoe707", password="strongpassword")

```