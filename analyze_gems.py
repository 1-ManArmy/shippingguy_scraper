#!/usr/bin/env python3
"""
Hidden Gems Analyzer - Analyze and categorize the extracted backend data
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class HiddenGemsAnalyzer:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.analysis_results = defaultdict(list)
        
    def analyze_booking_ids(self):
        """Analyze booking IDs and confirmation codes"""
        bookings_dir = self.data_dir / "bookings"
        confirmations_dir = self.data_dir / "confirmations"
        
        booking_patterns = {
            "booking_id": r"^[A-Z0-9]{8,12}$",
            "confirmation_code": r"^[A-Z0-9]{6,10}$",
            "pin_code": r"^[0-9]{4,8}$",
            "reference_number": r"^[A-Z]{2}[0-9]{6,8}$"
        }
        
        for directory in [bookings_dir, confirmations_dir]:
            if directory.exists():
                for file in directory.glob("*.json"):
                    with open(file) as f:
                        data = json.load(f)
                        for item in data:
                            for pattern_name, pattern in booking_patterns.items():
                                if re.match(pattern, str(item)):
                                    self.analysis_results[pattern_name].append({
                                        "value": item,
                                        "source_file": file.name,
                                        "confidence": "high"
                                    })
    
    def analyze_customer_data(self):
        """Analyze customer and guest information"""
        customers_dir = self.data_dir / "customers"
        
        if customers_dir.exists():
            for file in customers_dir.glob("*.json"):
                with open(file) as f:
                    data = json.load(f)
                    for customer_data in data:
                        if isinstance(customer_data, dict):
                            # Analyze emails
                            if "emails" in customer_data:
                                for email in customer_data["emails"]:
                                    domain = email.split("@")[1] if "@" in email else ""
                                    self.analysis_results["customer_emails"].append({
                                        "email": email,
                                        "domain": domain,
                                        "source_file": file.name
                                    })
                            
                            # Analyze phone numbers
                            if "phones" in customer_data:
                                for phone in customer_data["phones"]:
                                    country_code = phone[:3] if phone.startswith("+") else "unknown"
                                    self.analysis_results["customer_phones"].append({
                                        "phone": phone,
                                        "country_code": country_code,
                                        "source_file": file.name
                                    })
                            
                            # Analyze names
                            if "names" in customer_data:
                                for name in customer_data["names"]:
                                    self.analysis_results["customer_names"].append({
                                        "name": name,
                                        "source_file": file.name
                                    })
    
    def analyze_payment_data(self):
        """Analyze payment and transaction information"""
        payment_dir = self.data_dir / "payment_data"
        
        if payment_dir.exists():
            for file in payment_dir.glob("*.json"):
                with open(file) as f:
                    data = json.load(f)
                    for payment_data in data:
                        if isinstance(payment_data, dict):
                            # Analyze payment IDs
                            if "payment" in payment_data:
                                for payment_id in payment_data["payment"]:
                                    self.analysis_results["payment_ids"].append({
                                        "payment_id": payment_id,
                                        "source_file": file.name
                                    })
                            
                            # Analyze transaction IDs
                            if "transaction" in payment_data:
                                for transaction_id in payment_data["transaction"]:
                                    self.analysis_results["transaction_ids"].append({
                                        "transaction_id": transaction_id,
                                        "source_file": file.name
                                    })
                            
                            # Analyze amounts
                            if "amount" in payment_data:
                                for amount in payment_data["amount"]:
                                    self.analysis_results["payment_amounts"].append({
                                        "amount": amount,
                                        "source_file": file.name
                                    })
    
    def analyze_hidden_apis(self):
        """Analyze hidden API endpoints"""
        hidden_apis_dir = self.data_dir / "hidden_apis"
        
        if hidden_apis_dir.exists():
            for file in hidden_apis_dir.glob("*.json"):
                with open(file) as f:
                    data = json.load(f)
                    for api_data in data:
                        if isinstance(api_data, dict):
                            for api_type, endpoints in api_data.items():
                                for endpoint in endpoints:
                                    risk_level = "high" if any(risk in endpoint for risk in ["admin", "internal", "debug"]) else "medium"
                                    self.analysis_results["hidden_endpoints"].append({
                                        "endpoint": endpoint,
                                        "type": api_type,
                                        "risk_level": risk_level,
                                        "source_file": file.name
                                    })
    
    def analyze_auth_tokens(self):
        """Analyze authentication tokens and session data"""
        auth_dir = self.data_dir / "auth_tokens"
        
        if auth_dir.exists():
            for file in auth_dir.glob("*.json"):
                with open(file) as f:
                    data = json.load(f)
                    for auth_data in data:
                        if isinstance(auth_data, dict):
                            for token_type, tokens in auth_data.items():
                                for token in tokens:
                                    token_length = len(token)
                                    token_entropy = self.calculate_entropy(token)
                                    self.analysis_results["auth_tokens"].append({
                                        "token": token[:10] + "..." if len(token) > 10 else token,
                                        "type": token_type,
                                        "length": token_length,
                                        "entropy": token_entropy,
                                        "source_file": file.name
                                    })
    
    def analyze_debug_info(self):
        """Analyze debug information and potential vulnerabilities"""
        debug_dir = self.data_dir / "debug_info"
        
        vulnerability_patterns = {
            "sql_injection": r"sql|database|query|select|insert|update|delete",
            "path_disclosure": r"[a-zA-Z]:\\|\/[a-zA-Z]",
            "stack_trace": r"at\s+[a-zA-Z]|traceback|exception",
            "configuration_leak": r"password|secret|key|token|config"
        }
        
        if debug_dir.exists():
            for file in debug_dir.glob("*.json"):
                with open(file) as f:
                    data = json.load(f)
                    for debug_data in data:
                        if isinstance(debug_data, dict):
                            for info_type, info_list in debug_data.items():
                                for info in info_list:
                                    info_lower = info.lower()
                                    for vuln_type, pattern in vulnerability_patterns.items():
                                        if re.search(pattern, info_lower):
                                            self.analysis_results["potential_vulnerabilities"].append({
                                                "type": vuln_type,
                                                "info": info[:100] + "..." if len(info) > 100 else info,
                                                "source_file": file.name
                                            })
    
    def calculate_entropy(self, data):
        """Calculate entropy of a string"""
        import math
        if not data:
            return 0
        
        counts = {}
        for char in data:
            counts[char] = counts.get(char, 0) + 1
        
        entropy = 0
        for count in counts.values():
            p = count / len(data)
            entropy -= p * math.log2(p)
        
        return round(entropy, 2)
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_booking_ids": len(self.analysis_results["booking_id"]),
                "total_confirmation_codes": len(self.analysis_results["confirmation_code"]),
                "total_customer_emails": len(self.analysis_results["customer_emails"]),
                "total_customer_phones": len(self.analysis_results["customer_phones"]),
                "total_payment_ids": len(self.analysis_results["payment_ids"]),
                "total_hidden_endpoints": len(self.analysis_results["hidden_endpoints"]),
                "total_auth_tokens": len(self.analysis_results["auth_tokens"]),
                "total_vulnerabilities": len(self.analysis_results["potential_vulnerabilities"])
            },
            "details": dict(self.analysis_results)
        }
        
        return report
    
    def save_report(self, filename=None):
        """Save analysis report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hidden_gems_analysis_{timestamp}.json"
        
        report = self.generate_report()
        reports_dir = self.data_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / filename
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Analysis report saved: {report_file}")
        return report_file
    
    def run_full_analysis(self):
        """Run complete analysis of all hidden gems"""
        print("🔍 Starting hidden gems analysis...")
        
        self.analyze_booking_ids()
        print("✅ Booking IDs analyzed")
        
        self.analyze_customer_data()
        print("✅ Customer data analyzed")
        
        self.analyze_payment_data()
        print("✅ Payment data analyzed")
        
        self.analyze_hidden_apis()
        print("✅ Hidden APIs analyzed")
        
        self.analyze_auth_tokens()
        print("✅ Auth tokens analyzed")
        
        self.analyze_debug_info()
        print("✅ Debug info analyzed")
        
        report_file = self.save_report()
        print(f"🎉 Analysis complete! Report saved to: {report_file}")
        
        # Print summary
        report = self.generate_report()
        print("\n📈 Analysis Summary:")
        for key, value in report["summary"].items():
            print(f"  {key}: {value}")

def main():
    analyzer = HiddenGemsAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
