def format_storage_size(size_in_gb):
    if size_in_gb >= 1000:
        return str(size_in_gb / 1000) + ' ТБ'
    else:
        return str(size_in_gb) + ' ГБ'
