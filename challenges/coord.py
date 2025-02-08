from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import pandas as pd

def plot_characters_from_google_docs(url):
    """
    Plots characters from a Google Docs table.

    Args:
        url: The URL of the published Google Doc.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')

        if table is None:
            print("Error: No table found on the page.")
            return

        headers = [header.text for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 0:
                rows.append([cell.text for cell in cells])

        if not rows:
            print("Error: No data rows found in the table.")
            return

        df = pd.DataFrame(rows, columns=headers if headers else ['x-coordinate', 'Character', 'y-coordinate']) #Handles cases where there are no headers


        df['x-coordinate'] = pd.to_numeric(df['x-coordinate'], errors='coerce')
        df['y-coordinate'] = pd.to_numeric(df['y-coordinate'], errors='coerce')


        plt.figure(figsize=(15, 10))

        for x, y, char in zip(df['x-coordinate'], df['y-coordinate'], df['Character']):
            if pd.notna(x) and pd.notna(y) and char: #added a check to skip nan values and empty strings
                plt.text(x, y, char, ha='center', va='center', fontsize=20)

        plt.xlim(df['x-coordinate'].min() - 0.5, df['x-coordinate'].max() + 0.5)
        plt.ylim(df['y-coordinate'].min() - 0.5, df['y-coordinate'].max() + 0.5)
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title('Character Plot')
        plt.grid(True)
        plt.gca().set_aspect('equal')
        plt.show()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage:
url = "https://docs.google.com/document/d/e/2PACX-1vSZ1vDD85PCR1d5QC2XwbXClC1Kuh3a4u0y3VbTvTFQI53erafhUkGot24ulET8ZRqFSzYoi3pLTGwM/pub"
plot_characters_from_google_docs(url)
