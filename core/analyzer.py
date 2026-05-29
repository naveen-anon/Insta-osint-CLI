import re

class IntelAnalyzer:
    @staticmethod
    def extract_behavioral_keywords(biography_text):
        """Bio analytics aur potential indicators extract karta hai"""
        if not biography_text:
            return {"keywords": [], "total_words": 0}
            
        # Clean and tokenize words
        words = re.findall(r'\b\w+\b', biography_text.lower())
        total_words = len(words)
        
        # Word frequency counter mapping
        freq_map = {}
        for word in words:
            if len(word) > 2: # short words ignore karne ke liye
                freq_map[word] = freq_map.get(word, 0) + 1
                
        sorted_keywords = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)
        return {
            "keywords": sorted_keywords[:10], # Top 10 weights
            "total_words": total_words
        }
      
