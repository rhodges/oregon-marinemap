
port_names = ['Astoria', 'Depoe Bay', 'Newport', 'Florence', 'SOORC Ports', 'Gold Beach & Brookings']
port_abbrs = {  'Astoria': 'astr', 
                'Depoe Bay': 'dpor', 
                'Newport': 'newr', 
                'Florence': 'flrr', 
                'SOORC Ports': 'srcr', 
                'Gold Beach & Brookings': 'bgdr' }

fisheries = [   ('Dungeness', 'dcrab'),
                ('Pacific Halibut', 'phal'), 
                ('Rockfish', 'rckf'),
                ('Salmon', 'sal')]                     

multipliers = { 'dcrab': 1.55,
                'phal': 1.55, 
                'rckf': 1.55, 
                'sal': 1.55  } 
                
charter_totals = {  'astr':{'dcrab':38724.25,
                            'phal': 249856.34, 
                            'rckf': 383190.32, 
                            'sal' : 1547455.59 },                  
                    'bgdr':{'dcrab':41984.30,
                            'rckf': 78607.73, 
                            'sal' : 79674.42 },                
                    'dpor':{'dcrab':137111.41, 
                            'phal': 372500.83, 
                            'rckf': 507692.63, 
                            'sal' : 211195.13 },                
                    'flrr':{'dcrab':1184.03, 
                            'phal': 11696.00, 
                            'rckf': 746.74, 
                            'sal' : 2373.23 },              
                    'newr':{'dcrab':184982.96, 
                            'phal': 615032.73, 
                            'rckf': 606474.95, 
                            'sal' : 191466.03 },             
                    'srcr':{'dcrab':109526.23, 
                            'phal': 228010.54, 
                            'rckf': 227032.91, 
                            'sal' : 228136.53 },
                    'state':{'dcrab':513513.18, 
                             'phal': 1477096.44, 
                             'rckf': 1803745.27, 
                             'sal' : 2260300.94 }
                 }                