import requests
import json

class LocationFinder:
    def __init__(self):
        self.base_url = "https://api.postalpincode.in/pincode/"
        
    def find_location_by_pincode(self, pincode):
        """Find location details using Indian pincode"""
        try:
            # Clean pincode
            pincode = str(pincode).strip()
            
            # API call to get location data
            response = requests.get(f"{self.base_url}{pincode}", timeout=5)
            data = response.json()
            
            if data and data[0]['Status'] == 'Success':
                location_data = data[0]['PostOffice'][0]
                
                location_info = {
                    'pincode': pincode,
                    'area': location_data['Name'],
                    'district': location_data['District'],
                    'state': location_data['State'],
                    'country': location_data['Country'],
                    'division': location_data.get('Division', 'N/A')
                }
                
                return location_info
            else:
                return None
                
        except Exception as e:
            print(f"Location search failed: {e}")
            return None
    
    def get_google_maps_link(self, location_info):
        """Generate Google Maps link for the location"""
        if not location_info:
            return None
            
        # Create search query for Google Maps
        query = f"{location_info['area']}, {location_info['district']}, {location_info['state']}, India"
        encoded_query = query.replace(' ', '+')
        
        google_maps_url = f"https://www.google.com/maps/search/{encoded_query}"
        return google_maps_url
    
    def format_location_response(self, location_info):
        """Format location information for display"""
        if not location_info:
            return "Location not found for this pincode."
        
        response = f"""Location Details:
📍 Area: {location_info['area']}
🏘️ District: {location_info['district']}
🏛️ State: {location_info['state']}
🌏 Country: {location_info['country']}
📮 Pincode: {location_info['pincode']}

Google Maps: {self.get_google_maps_link(location_info)}"""
        
        return response