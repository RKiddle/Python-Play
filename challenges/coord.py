from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

def plot_characters_from_google_doc(doc_url):
    """Plots characters from a table in a Google Doc.

    Args:
        doc_url: The URL of the Google Doc (in published format).

    Returns:
       None. Displays the plot.  Prints error messages to the console if there are issues.
    """
    try:
        response = requests.get(doc_url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')

        if not table:
            raise ValueError("Table not found in the document.")

        headers = [th.text for th in table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:  # Only process rows with data cells
                rows.append([cell.text for cell in cells])

        if not rows:
          raise ValueError("No data rows found in the table.")

        df = pd.DataFrame(rows, columns=headers)

        # Convert to numeric, handle errors, and remove rows with NaNs
        df['x-coordinate'] = pd.to_numeric(df['x-coordinate'], errors='coerce').astype('Int64')
        df['y-coordinate'] = pd.to_numeric(df['y-coordinate'], errors='coerce').astype('Int64')
        df.dropna(inplace=True)

        # Plotting
        plt.figure(figsize=(6, 4))
        for x, y, char in zip(df['x-coordinate'], df['y-coordinate'], df['Character']):
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
        print(f"Error fetching document: {e}")
    except ValueError as e:
        print(f"Error processing data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage:
if __name__ == "__main__":
    google_doc_url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"  # Replace with your URL
    plot_characters_from_google_doc(google_doc_url)

    # Example with a different URL:
    # another_url = "your_other_url"
    # plot_characters_from_google_doc(another_url)
