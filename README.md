# Migración de políticas de Avamar

Script en Python para facilitar la migración de políticas (grupos) entre servidores Avamar. En lugar de escribir a mano un comando por cada política, el script los genera a partir de la lista de grupos del servidor.

## Qué hace

Al ejecutarlo muestra un menú con tres opciones:

1. **Exportación de políticas:** consulta los grupos con `mccli group show` (de todos los dominios o de uno) y muestra el comando `mccli group export` de cada política, que guarda un archivo XML en `/tmp/policies`.
2. **Transferir archivos exportados:** copia los XML al servidor Avamar de destino con `scp`.
3. **Importación de políticas:** consulta los grupos y muestra el comando `mccli mcs import` de cada política, para ejecutarlo en el servidor de destino.

## Requisitos

- Python 3
- Un servidor Linux con Avamar y la herramienta `mccli`
- Acceso por SSH al servidor de destino (para la opción 2)

## Uso

```bash
python3 avamar_policies.py
```

Elige una opción del menú y responde a las preguntas. Los comandos generados se copian y se ejecutan en el servidor correspondiente.

## Nota

Es una herramienta genérica de automatización. No contiene datos de clientes, nombres de servidores ni credenciales.