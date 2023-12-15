#!/usr/bin/python3

def build_patch_panel(db):
    """Build the patch panel data structure for table rendering."""
    with open('templates/patch_table_row.html', 'r') as f:
        patch_table_row = f.read()

    patch_panel_db = db.dgetall('patch')
    patch_panel_table = ''

    for port in sorted(patch_panel_db.keys(), key=lambda x: int(x)):
        patch_panel_table += patch_table_row.format(port, patch_panel_db[port])
    
    return patch_panel_table