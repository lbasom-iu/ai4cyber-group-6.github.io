import requests
import pandas as pd

def fetch_cves_with_scores(keywords, target_count=50):
    collected_data = []
    seen_descriptions = set()
    results_per_page = 100
    total_fetched = 0

    for keyword in keywords:
        while len(collected_data) < target_count:
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage={results_per_page}&startIndex={total_fetched}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])
                
                for item in vulnerabilities:
                    descriptions = [desc['value'] for desc in item['cve']['descriptions'] if desc['lang'] == 'en']
                    if not descriptions:
                        continue  # Skip if there are no descriptions
                    
                    description = descriptions[0].strip()
                    if description in seen_descriptions:
                        continue  # Skip if the description is a duplicate
                    
                    if 'cvssMetricV31' in item['cve']['metrics'] or 'cvssMetricV3' in item['cve']['metrics']:
                        seen_descriptions.add(description)
                        collected_data.append(item)
                        if len(collected_data) == target_count:
                            break
                
                total_fetched += len(vulnerabilities)
                if not vulnerabilities:
                    break  # Exit the loop if no more data is returned
            else:
                print(f"Failed to fetch data for '{keyword}': HTTP {response.status_code}")
                break  # Exit on HTTP error
            
            if len(collected_data) == target_count:
                break  # Exit the loop if we've collected enough data

    return collected_data[:target_count]

def process_cves_data(cve_items):
    records = []
    for item in cve_items:
        cve_id = item['cve']['id']
        published_date = item['cve']['published']
        last_modified = item['cve']['lastModified']
        description = next((desc['value'] for desc in item['cve']['descriptions'] if desc['lang'] == 'en'), "")
        
        cvss_score = "N/A"
        base_severity = "N/A"
        metrics = item['cve'].get('metrics', {})
        if 'cvssMetricV31' in metrics:
            cvss_data = metrics['cvssMetricV31'][0]['cvssData']
            cvss_score = cvss_data.get('baseScore', 'N/A')
            base_severity = cvss_data.get('baseSeverity', 'N/A')
        elif 'cvssMetricV3' in metrics:
            cvss_data = metrics['cvssMetricV3'][0]['cvssData']
            cvss_score = cvss_data.get('baseScore', 'N/A')
            base_severity = cvss_data.get('baseSeverity', 'N/A')
        
        records.append({
            "CVE ID": cve_id,
            "Published Date": published_date,
            "Last Modified": last_modified,
            "Description": description,
            "CVSS Score": cvss_score,
            "Base Severity": base_severity
        })
    
    return pd.DataFrame(records)

# Define your search terms
search_terms = ["Healthcare", "Hospital", "EMR", "HIPAA", "Medical Device", "Hospital Information System"]

# Fetch and process the CVE data
cve_items_with_scores = fetch_cves_with_scores(search_terms, 50)
df_cves_with_scores = process_cves_data(cve_items_with_scores)

# Display the DataFrame
print(df_cves_with_scores)

# Save the DataFrame to a CSV file
df_cves_with_scores.to_csv('cves_with_cvss_scores_detailed_no_duplicates.csv', index=False)
print("CVE data saved to 'cves_with_cvss_scores_detailed_no_duplicates.csv'")
