# FP-Growth-Based-Web-Log-Analysis-Project
This project is based on Association Rule Mining using the FP-Growth Algorithm on a Web Log dataset. The project includes a user-friendly GUI for uploading datasets, running the mining algorithm, visualizing patterns, and generating page recommendations.
💻 FP-Growth Based Web Log Analysis Project

This project is based on Association Rule Mining using the FP-Growth Algorithm on a Web Log dataset.
It finds frequent user navigation patterns on a website — identifying which pages users visit together and in what order.
The project also includes a user-friendly GUI for uploading datasets, running the mining algorithm, visualizing patterns, and generating page recommendations.

Project Objective

To analyze user browsing behavior from web log data using the FP-Growth algorithm and present results through an interactive dashboard.

The goal is to:
Understand user navigation patterns
Improve website structure
Provide personalized recommendations
Enhance user experience
Modules in the Project
Dataset Selection Panel
Upload or select the Web Log dataset (CSV).
Preview total sessions, pages, and visit counts with charts.
Mining Panel (Algorithm Execution)
Uses FP-Growth for mining frequent itemsets and generating association rules.
Parameters: Minimum Support = 0.2, Minimum Confidence = 0.6
Displays progress and number of rules generated.
Rules Table Output
Shows generated association rules with Support, Confidence, and Lift.

Example:
{Home, Product} → {Add to Cart} → Users visiting Home and Product pages often go to Add to Cart.

Visualization Panel:
Bar charts for top rules by confidence.

Network graph showing the flow between pages:
(Home) → (Product) → (Add to Cart) → (Checkout).
Node color intensity and edge thickness represent support and confidence.

Recommendation Panel:
Suggests the next likely page based on user selections.

Example:
If user selects Home + Product → Recommended: Add to Cart.

Export Panel:
Exports mined rules and patterns as CSV file (association_rules.csv).
Columns: antecedents, consequents, support, confidence, lift.

Technology Used:
Language: Python
Libraries: tkinter, pandas, matplotlib, mlxtend (for FP-Growth), networkx
Algorithm: FP-Growth (Frequent Pattern Growth)

Why FP-Growth?
Faster than Apriori (no repeated candidate generation).
Builds a compact FP-tree data structure.
Scans dataset only twice.
Handles large data efficiently.

Features:
Interactive GUI for data mining
Real-time visualizations and rule tables
Page recommendations using mined rules
Exportable results for reports
Easy parameter customization

Applications:
Website structure optimization
E-commerce recommendation systems
Clickstream behavior analysis
Personalized user experience design

Methodology:
<img width="843" height="488" alt="{ED61A10B-8474-4CE0-A20C-6CC448EEEEBA}" src="https://github.com/user-attachments/assets/db38c045-1e6b-4e9e-a24f-c54cdd59c945" />

Screenshots:
<img width="1911" height="862" alt="{86BCD01F-ADB1-4830-B37E-45C3AAA407B2}" src="https://github.com/user-attachments/assets/4578f17a-6111-40ba-9b27-69959bab6046" />

<img width="1916" height="853" alt="{3000AC11-E211-45E0-8734-B20584A17B61}" src="https://github.com/user-attachments/assets/d24470e2-ac2c-4338-8bed-f094f1f75118" />

<img width="1596" height="728" alt="{CC8764F9-B31E-4A9F-86F6-53E55B89C397}" src="https://github.com/user-attachments/assets/58b74704-af65-4cb2-bbd0-51da859f489c" />

<img width="976" height="634" alt="{9E3CA3FA-C08A-4ADC-96E0-A9770B1B67B7}" src="https://github.com/user-attachments/assets/39cb9afc-2e5b-4fdf-9525-ef94b2ac3b1b" />

<img width="1824" height="696" alt="{54B6D480-10BF-4ABE-AA5B-1F5981D957E3}" src="https://github.com/user-attachments/assets/a113d82b-2a0e-4a48-9f1e-4886b80201ba" />

<img width="1847" height="663" alt="{D9EF5E78-0D77-4D16-8791-A34D5EE9DAA3}" src="https://github.com/user-attachments/assets/c5217571-4ce7-44b4-90bd-f517350557e4" />

Developer

Aishwarya Marshettiwar
FP-Growth Web Log Analysis Project — developed for learning and demonstration of Association Rule Mining concepts.

Future Enhancements:
Real-time log analysis
Integration with web analytics tools
Cloud-based data storage and processing
Dynamic visualization dashboard
