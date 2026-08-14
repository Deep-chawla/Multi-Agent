import re

class TextCleaner:
    def clean_documents(self, documents):
        for doc in documents:
            text = doc.page_content

            # Remove extra spaces/tabs
            text = re.sub(r'[ \t]+', ' ', text)

            # Remove repeated blank lines
            text = re.sub(r'\n+', '\n', text)

            # Remove leading/trailing spaces
            text = text.strip()

            # Update cleaned content
            doc.page_content = text

        return documents
   
   
    def remove_duplicate_lines(self, documents):
        for doc in documents:
            lines = doc.page_content.splitlines()
            unique_lines = []
            previous_line = ""
            for line in lines:
                cleaned = line.strip()
                if cleaned and cleaned != previous_line:
                    unique_lines.append(cleaned)
                previous_line = cleaned

            doc.page_content = "\n".join(unique_lines)
        return documents
    

 