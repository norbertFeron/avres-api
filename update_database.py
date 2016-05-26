from importer.importFromJson import ImportFromJson

if __name__ == '__main__':
    importer = ImportFromJson()
    importer.create_users()
    importer.create_posts()
    importer.create_comments()
