from app.models.new_comer import NewComer

def format_new_comer(data:NewComer):
    return {
        "id": data.id,
        "name": data.name,
        "birthday":data.birthday.isoformat(),
        "phone":data.phone,
        "p_address":data.p_address,
        "m_address":data.m_address,
        "email":data.email,
        "baptized":data.baptized,
        "registered_at":data.registered_at.isoformat()
    }

def format_new_comers(data):
    return [format_new_comer(d) for d in data]

def format_new_comer_for_google_sheet(data:NewComer):
    return [data.registered_at.isoformat(), data.name, data.birthday.isoformat(), data.phone, data.p_address, data.m_address, data.email, data.baptized]

def format_new_comers_for_google_sheet(data):
    return [format_new_comer_for_google_sheet(item) for item in data ]
