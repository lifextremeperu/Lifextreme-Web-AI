import urllib.request
import json

print("=" * 50)
print("  Lifextreme - Obtener Page Access Token")
print("=" * 50)
token = input("\nPega tu User Token (EAAR...): ").strip()

url = "https://graph.facebook.com/v19.0/me/accounts?access_token=" + token

try:
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
        pages = data.get("data", [])
        
        if not pages:
            print("\nNo se encontraron paginas. Verifica que el token sea correcto.")
        else:
            print(f"\nSe encontraron {len(pages)} pagina(s):\n")
            for page in pages:
                print("--- PAGINA: " + page["name"] + " ---")
                print("Page ID    : " + page["id"])
                print("Page Token : " + page["access_token"])
                print()
except Exception as e:
    print("\nError: " + str(e))
    print("Verifica que el token sea valido y no haya expirado.")
