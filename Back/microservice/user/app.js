const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

// Configura la conexión a la base de datos PostgreSQL
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'proyecto',
  password: 'admin',
  port: 5432,
});
app.use(cors());
// Middleware para procesar el cuerpo de las solicitudes como JSON
app.use(express.json());

// Ruta para obtener todos los usuarios (GET)
app.get('/usuarios', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuario');
    res.json(result.rows);
  } catch (err) {
    console.error('Error al obtener los usuarios:', err);
    res.status(500).json({ error: 'Error al obtener los usuarios' });
  }
});

// Ruta para crear un nuevo usuario (POST)
app.post('/crear_usuarios', async (req, res) => {
  const { email, contrasenia } = req.body;
  try {
    await pool.query(
      'INSERT INTO usuario (email, contrasenia) VALUES ($1, $2)',
      [email, contrasenia]
    );
    res.json({ mensaje: 'Usuario creado correctamente' });
  } catch (err) {
    console.error('Error al crear el usuario:', err);
    res.status(500).json({ error: 'Error al crear el usuario' });
  }
});

app.post('/verificar_usuario', async (req, res) => {
  const { email, contrasenia } = req.body;
  try {
    const result = await pool.query(
      'SELECT * FROM usuario WHERE email = $1 AND contrasenia = $2',
      [email, contrasenia]
    );

    if (result.rows.length > 0) {
      // Si el usuario existe, devolvemos una respuesta con un mensaje indicando que el usuario existe
      res.json({ mensaje: 'Usuario existente' });
    } else {
      // Si el usuario no existe, devolvemos una respuesta con un mensaje indicando que el usuario no existe
      res.json({ mensaje: 'Usuario no existe' });
    }
  } catch (err) {
    console.error('Error al verificar el usuario:', err);
    res.status(500).json({ error: 'Error al verificar el usuario' });
  }
});

// Inicia el servidor
app.listen(port, () => {
  console.log(`Servidor API corriendo en http://localhost:${port}`);
});
