from datetime import datetime

def analyze_metadata(exif_data):
    """Analyze metadata for originality, AI generation, and tampering."""
    issues, risk_score, analyze_metadata_status = [], 0, 1
    if not exif_data:
        issues.append("No EXIF data found - Could be AI-generated or manipulated.")
        risk_score += 2
        analyze_metadata_status = 0
        return issues, risk_score, analyze_metadata_status

    camera_make = exif_data.get('Make', None)
    camera_model = exif_data.get('Model', None)
    creation_date = exif_data.get('DateTime', None)
    modification_date = exif_data.get('DateTimeDigitized', None)

    if camera_make is None or camera_model is None:
        issues.append("Camera make/model missing - Could indicate tampering or AI generation.")
        risk_score += 2

    if creation_date and modification_date:
        try:
            creation_dt = datetime.strptime(creation_date, "%Y:%m:%d %H:%M:%S")
            modification_dt = datetime.strptime(modification_date, "%Y:%m:%d %H:%M:%S")
            if (modification_dt - creation_dt).total_seconds() > 60:
                issues.append("Significant modification after creation")
                risk_score += 1
        except Exception as e:
            issues.append(f"Date parsing issue: {e}")
            risk_score += 1
    else:
        issues.append("Missing creation or modification date")
        risk_score += 1

    gps_info = exif_data.get('GPSInfo', None)
    if not gps_info:
        issues.append("No GPS location data")
        risk_score += 1

    software = exif_data.get('Software', None)
    if software:
        if any(keyword in software for keyword in ("Adobe", "GIMP", "Photoshop")):
            issues.append(f"Edited with {software}")
            risk_score += 2
    else:
        issues.append("No editing software info")

    return issues, risk_score, analyze_metadata_status