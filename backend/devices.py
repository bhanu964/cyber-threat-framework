from datetime import datetime, timezone

from backend.database import get_connection


def register_device(
    device_id: str,
    platform: str,
    role: str = "victim"
):
    now = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO devices (
            device_id,
            platform,
            role,
            status,
            registered_at,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(device_id)
        DO UPDATE SET
            platform = excluded.platform,
            role = excluded.role,
            status = 'online',
            last_seen = excluded.last_seen
    """, (
        device_id,
        platform,
        role,
        "online",
        now,
        now
    ))

    connection.commit()

    cursor.execute(
        "SELECT * FROM devices WHERE device_id = ?",
        (device_id,)
    )

    device = dict(cursor.fetchone())

    connection.close()

    return device


def get_devices():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM devices
        ORDER BY registered_at ASC
    """)

    devices = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return devices


def get_device(device_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM devices
        WHERE device_id = ?
    """, (device_id,))

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None


def update_heartbeat(device_id: str):

    now = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE devices

        SET
            last_seen = ?,
            status = 'online'

        WHERE device_id = ?
    """, (
        now,
        device_id
    ))

    connection.commit()

    cursor.execute("""
        SELECT *
        FROM devices
        WHERE device_id = ?
    """, (device_id,))

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None