with open('hub.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace Pilar 2 link and text
c = c.replace('href="https://studio.lifextreme.store" target="_blank"', 'href="/studio"')
c = c.replace('● 38 MODELOS', '● OPEN-HIGGSFIELD')

# Replace Pilar 3 link and text
c = c.replace('href="/vr-experience.html"', 'href="/geoint"')
c = c.replace('● 3D GEOINT', '● 3D WAR ROOM')
c = c.replace('Acceder al War Room 3D ➔', 'Acceder al War Room 3D (Cámaras) ➔')

with open('hub.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('hub.html successfully updated with operational links')
