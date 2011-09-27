
port_names = ['Astoria', 'Garibaldi/Tillamook', 'Salmon River', 'Depoe Bay', 'Newport', 'Florence', 'SOORC Ports', 'Gold Beach & Brookings']
port_abbrs = {  'Astoria': 'astr', 
                'Garibaldi/Tillamook': 'tllr', 
                'Salmon River': 'slmr', 
                'Depoe Bay': 'dpor', 
                'Newport': 'newr', 
                'Florence': 'flrr', 
                'SOORC Ports': 'srcr', 
                'Gold Beach & Brookings': 'bgdr' }

fisheries = [   #('Dungeness crab', 'dcrab'),
                #('Flatfish', 'flat'), 
                ('Pacific Halibut', 'phal'),
                ('Rockfish', 'rckf'),
                ('Salmon', 'sal') ]                     

multipliers = { 'dcrab': 1., 
                'flat': 1., 
                'phal': 1., 
                'rckf': 1., 
                'sal': 1.  } 
                
rec_totals = {  'astr':{'rckf': 8366.23, 
                        'phal': 2218.81, 
                        'sal' : 424370.3 },                  
                'dpor':{'rckf': 62960.00, 
                        'phal': 15202.03, 
                        'sal' : 138881.11 },                  
                'flrr':{'rckf': 404.27, 
                        'phal': 4566.23, 
                        'sal' : 69034.01 },                  
                'tllr':{'rckf': 75446.46, 
                        'phal': 49735.99, 
                        'sal' : 404925.52 },                 
                'bgdr':{'rckf': 827634.74,
                        'sal' : 333832.26 },                 
                'newr':{'rckf': 170773.73, 
                        'phal': 270325.95, 
                        'sal' : 383583.05 },                 
                'slmr':{'rckf': 123421.52, 
                        'phal': 10029.89, 
                        'sal' : 102155.48 },                 
                'srcr':{'rckf': 261089.96, 
                        'phal': 36929.97, 
                        'sal' : 868692.54 },
                'state':{'rckf':1530096.91,
                         'phal':389008.87,
                         'sal' :2725474.26 }
            }