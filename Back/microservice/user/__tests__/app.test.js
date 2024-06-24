const request = require('supertest')
const app = require('../app')
//const Test = require('supertest/lib/test')

//prueba jest para la obtención de los usuarios 
describe('GET /usuarios', () =>{
    test('Este caso de prueba unitaria debe traer a los usuarios de manera de array porque el api esta estructurado', async () =>{
        const response = await request(app).get('/usuarios');
        expect(response.statusCode).toBe(200)
        expect(response.body).toBeInstanceOf(Array)

    })
})