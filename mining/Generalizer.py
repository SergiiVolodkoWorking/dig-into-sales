class Generalizer():
    @staticmethod
    def generalize_headquarter(linkedin_hq):
        linkedin_hq = linkedin_hq.replace('California', 'CA')
        linkedin_hq = linkedin_hq.replace('Florida', 'FL')
        linkedin_hq = linkedin_hq.replace('Ohio', 'OH')
        linkedin_hq = linkedin_hq.replace('Illinois', 'IL')
        linkedin_hq = linkedin_hq.replace('Pennslyvania', 'PA')
        linkedin_hq = linkedin_hq.replace('Virginia', 'VA')
        linkedin_hq = linkedin_hq.replace('Arkansas', 'AR')
        linkedin_hq = linkedin_hq.replace('North Carolina', 'NC')
        linkedin_hq = linkedin_hq.replace('Massachusetts', 'MA')
        linkedin_hq = linkedin_hq.replace('TX - Texas', 'TX').replace('Texas', 'TX')
        linkedin_hq = linkedin_hq.replace('England', 'UK').replace('Essex', 'UK').replace('Cambridgeshire', 'UK')
        
        mappings = [
            {
                'words': ['london'],
                'hq': 'London, UK'
            },
            {
                'words': ['new york', 'brooklyn', 'ny, ny'],
                'hq': 'New York, NY'
            },
            {
                'words': ['san francisco'],
                'hq': 'San Francisco, CA'
            },
            {
                'words': ['berlin'],
                'hq': 'Berlin, Germany'
            },
            {
                'words': ['paris'],
                'hq': 'Paris, France'
            },
            {
                'words': ['warszawa', 'warsaw'],
                'hq': 'Warsaw, Poland'
            },
            {
                'words': ['toronto'],
                'hq': 'Toronto, Ontario'
            },
            {
                'words': ['bristol'],
                'hq': 'Bristol'
            },
            {
                'words': ['manchester'],
                'hq': 'Manchester, UK'
            },
            {
                'words': ['guildford'],
                'hq': 'Guildford, UK'
            },
            {
                'words': ['boston'],
                'hq': 'Boston, MA'
            },
            {
                'words': ['singapore'],
                'hq': 'Singapore'
            },
            {
                'words': ['new delhi'],
                'hq': 'New Delhi'
            },
            {
                'words': ['chicago'],
                'hq': 'Chicago, IL'
            },
            {
                'words': ['austin'],
                'hq': 'Austin, TX'
            },
            {
                'words': ['seattle'],
                'hq': 'Seattle, WA'
            },
            {
                'words': ['madison'],
                'hq': 'Madison, WI'
            },
            {
                'words': ['washington'],
                'hq': 'Washington, DC'
            },
            {
                'words': ['atlanta'],
                'hq': 'Atlanta, GA'
            },
            {
                'words': ['northbrook'],
                'hq': 'Northbrook, IL'
            },
            {
                'words': ['nashville'],
                'hq': 'Nashville, TN'
            },
            {
                'words': ['fremont'],
                'hq': 'Fremont, CA'
            },
            {
                'words': ['irvine'],
                'hq': 'Irvine, CA'
            },
            {
                'words': ['dallas'],
                'hq': 'Dallas, TX'
            },
            {
                'words': ['miami'],
                'hq': 'Miami, FL'
            },
            {
                'words': ['ann arbor'],
                'hq': 'Ann Arbor, MI'
            },
            {
                'words': ['lancaster'],
                'hq': 'Lancaster, PA'
            },
            {
                'words': ['philadelphia'],
                'hq': 'Philadelphia, PA'
            },
            {
                'words': ['indianapolis'],
                'hq': 'Indianapolis, IN'
            },
            {
                'words': ['bangalore'],
                'hq': 'Bangalore, Karnataka'
            },
            {
                'words': ['san jose'],
                'hq': 'San Jose, CA'
            },
            {
                'words': ['mc lean', 'mclean'],
                'hq': 'Mc Lean, VA'
            },
            {
                'words': ['st. louis', 'st louis'],
                'hq': 'St. Louis, MO'
            },
            ]

        for mapping in mappings:
            if any(word in linkedin_hq.lower() for word in mapping['words']):
                return mapping['hq']

        return linkedin_hq