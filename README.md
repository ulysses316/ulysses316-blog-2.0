# Ulysses316

## Requerimientos para correr el programa

Lo primero que tendremos que hacer para poder volver a trabajar con esta página 
es asegurarnos de tener todas las dependencias instaladas.
Instalar los requerimientos de python via pip

`pip install -r requirements.txt`

Posteriormente instalar las dependencias del frontend en la ruta /blog/static
ya sea con yarn o con npm.

`yarn install` || `npm install`

Debemos de asegurarnos de exportar todas las variables de entorno necesarias para nuestro programa.

- `FLASK_APP`
- `SECRET_KEY`
- Esta puede llegar a variar `SQLALCHEMY_DATABASE_URI` || `DATABASE_URL`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`

Y en dado caso que estemos trabajando de manera local podemos añadir la variable
- `FLASK_DEBUG`

También podemos agregar directamente estos campos a nuestro código, pero ya es cuestión de como deseamos trabajar, pero se recomienda usar las variables de entorno para no subir a git algo erróneamente.

## Inicializar el programa.

Una vez que ya tenemos todo pre-configurado lo primero que tenemos que hacer es crear nuestra base de datos para guardar la información de las tablas generada con SQLAlchemy.
Si el siguiente comando no funciona puede que tengamos problemas con postgres asi que recomendamos ver la documentación.

[NOTA] El nombre de nuestra base de datos debe ir en nuestra variable de entorno `SQLALCHEMY_DATABASE_URI` asi que este paso solo se hace si no tenemos ya previamente una tabla.  
- `createdb <namedb>`
Posterior a eso corremos los siguientes comandos para realizar las migraciones correspondientes de las tablas en nuestro programa a la base de datos.   
- `flask db init`
- `flask db migrate`
- `flask db upgrade`

Por último ya podemos correr el comando `flask run` para ver nuestra página.