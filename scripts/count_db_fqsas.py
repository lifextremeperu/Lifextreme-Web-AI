import os
from dotenv import load_dotenv
from supabase import create_client, Client

def main():
    load_dotenv(r'c:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\.env')
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print('No credentials')
        return

    supabase: Client = create_client(supabase_url, supabase_key)

    countries = ["argentina", "bolivia", "chile", "colombia", "ecuador", "peru"]
    total = 0
    print("=== Conteo de FQSAs en Supabase por País ===")
    for country in countries:
        try:
            # We filter by text_content starting with 'País: [Country]'
            # or we can just fetch and count if supabase allows
            res = supabase.table('knowledge_vectors').select('vector_id', count='exact').ilike('vector_id', f'{country}%').execute()
            count = res.count
            print(f"{country.capitalize()}: {count}")
            total += count if count else 0
        except Exception as e:
            print(f"Error for {country}: {e}")
            
    print(f"Total: {total}")

if __name__ == "__main__":
    main()
