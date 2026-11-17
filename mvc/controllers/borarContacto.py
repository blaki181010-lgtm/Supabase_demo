
import os
import web

from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

render = web.template.render('views', base='layout')


class BorrarContacto:

    def __init__(self) -> None:
        try:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")

            if not url or not key:
                raise ValueError("Faltan las credenciales de Supabase")

            self.supabase: Client = create_client(url, key)

        except Exception as error:
            print(f"ERROR 300: {error}")
            raise


    def obtenerContacto(self, id_contacto: int):

        try:
            response = (
                self.supabase
                .table("contactos")
                .select("*")
                .eq("id_contacto", id_contacto)
                .execute()
            )

            if response.data:
                contacto = response.data[0]
                return contacto
            else:
                return None

        except Exception as error:
            print(f"ERROR 301: {error}")
            return None

 
    def GET(self, id_contacto: int):

        contacto = self.obtenerContacto(id_contacto)

        if contacto:
            return render.borrar_contacto(contacto)
        else:
            return "Contacto no encontrado"


    def POST(self, id_contacto: int):

        try:
            response = (
                self.supabase
                .table("contactos")
                .delete()
                .eq("id_contacto", id_contacto)
                .execute()
            )

            if response.data:
                print(f"Contacto {id_contacto} eliminado correctamente")
                raise web.seeother('/contactos')

            else:
                return "No se encontró el contacto para eliminar"

        except web.HTTPError:
            raise

        except Exception as error:
            print(f"ERROR 302: {error}")
            return "Error al eliminar el contacto"
