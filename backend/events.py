from datetime import datetime, timezone

from backend.database import get_connection


def create_event(
    event_type: str,
    source: str,
    target: str | None,
    severity: str,
    message: str
):
    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events (
            timestamp,
            event_type,
            source,
            target,
            severity,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        event_type,
        source,
        target,
        severity,
        message
    ))

    event_id = cursor.lastrowid

    connection.commit()

    cursor.execute("""
        SELECT *
        FROM events
        WHERE event_id = ?
    """, (event_id,))

    event = dict(cursor.fetchone())

    connection.close()

    return event


def get_events():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM events
        ORDER BY event_id ASC
    """)

    events = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return events


def clear_events():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM events
    """)

    connection.commit()

    connection.close()

    return {
        "status": "cleared"
    }