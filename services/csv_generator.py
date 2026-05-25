import pandas as pd


def generate_products_csv(products, output_path):
    df = pd.DataFrame(products)
    df.to_csv(output_path, index=False)

    return output_path