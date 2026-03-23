# Automated Document Processing Pipeline Diagram

The following diagram illustrates the flow of data through the system, from user upload to the final automated action.

```mermaid
graph TD
    A["Document Upload (PDF/Image)"] --> B["OCR Service"]
    B --> C{"Text Extracted?"}
    C -- No --> D["Error Response"]
    C -- Yes --> E["Field Extractor"]
    E --> F["Raw Data (Name, Amount, Date, ID)"]
    G("Validator")
    F --> G
    G --> H{"Is Data Valid?"}
    H -- No --> I["Automated Action: Manual Review Required"]
    H -- Yes --> J["Automated Action: Automated Processing & Integration"]
```



## Description of Stages
1. **OCR Service**: Utilizes PaddleOCR to extract text from images or PDFs in-memory.
2. **Field Extractor**: Uses Regex patterns to identify Name, Amount, Date, and ID.
3. **Validator**: Checks for data presence, format, and logical ranges.
4. **Action Engine**: Triggers business logic (e.g., Audit flags) based on validated data.
