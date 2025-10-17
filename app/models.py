from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, String, Text, DateTime, Date, Numeric, ForeignKey, UniqueConstraint

Base = declarative_base()


class Vessel(Base):
	__tablename__ = "vessel"

	vessel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	imo_no: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
	vessel_name: Mapped[str] = mapped_column(String(100), nullable=False)
	call_sign: Mapped[Optional[str]] = mapped_column(String(20))
	operator_name: Mapped[Optional[str]] = mapped_column(String(100))
	flag_state: Mapped[Optional[str]] = mapped_column(String(50))
	built_year: Mapped[Optional[int]] = mapped_column(Integer)
	capacity_teu: Mapped[Optional[int]] = mapped_column(Integer)
	loa_m: Mapped[Optional[float]] = mapped_column(Numeric(6, 2))
	beam_m: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
	draft_m: Mapped[Optional[float]] = mapped_column(Numeric(4, 2))
	last_port: Mapped[Optional[str]] = mapped_column(String(5))
	next_port: Mapped[Optional[str]] = mapped_column(String(5))
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	containers = relationship("Container", back_populates="vessel")
	edi_messages = relationship("EdiMessage", back_populates="vessel")
	api_events = relationship("ApiEvent", back_populates="vessel")


class Container(Base):
	__tablename__ = "container"

	container_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	cntr_no: Mapped[str] = mapped_column(String(11), nullable=False)
	iso_code: Mapped[str] = mapped_column(String(4), nullable=False)
	size_type: Mapped[str] = mapped_column(String(10), nullable=False)
	gross_weight_kg: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
	status: Mapped[str] = mapped_column(String(16), nullable=False)
	origin_port: Mapped[str] = mapped_column(String(5), nullable=False)
	tranship_port: Mapped[str] = mapped_column(String(5), nullable=False, default="SGSIN")
	destination_port: Mapped[str] = mapped_column(String(5), nullable=False)
	hazard_class: Mapped[Optional[str]] = mapped_column(String(10))
	vessel_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("vessel.vessel_id"))
	eta_ts: Mapped[Optional[datetime]] = mapped_column(DateTime)
	etd_ts: Mapped[Optional[datetime]] = mapped_column(DateTime)
	last_free_day: Mapped[Optional[Date]] = mapped_column(Date)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	vessel = relationship("Vessel", back_populates="containers")

	__table_args__ = (
		UniqueConstraint("cntr_no", "created_at", name="uq_container_cntr_created"),
	)


class EdiMessage(Base):
	__tablename__ = "edi_message"

	edi_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	container_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("container.container_id"))
	vessel_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("vessel.vessel_id"))
	message_type: Mapped[str] = mapped_column(String(16), nullable=False)
	direction: Mapped[str] = mapped_column(String(4), nullable=False)
	status: Mapped[str] = mapped_column(String(16), nullable=False, default="RECEIVED")
	message_ref: Mapped[str] = mapped_column(String(50), nullable=False)
	sender: Mapped[str] = mapped_column(String(100), nullable=False)
	receiver: Mapped[str] = mapped_column(String(100), nullable=False)
	sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	ack_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
	error_text: Mapped[Optional[str]] = mapped_column(String(500))
	raw_text: Mapped[Optional[str]] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	vessel = relationship("Vessel", back_populates="edi_messages")
	container = relationship("Container")


class ApiEvent(Base):
	__tablename__ = "api_event"

	api_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	container_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("container.container_id"))
	vessel_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("vessel.vessel_id"))
	event_type: Mapped[str] = mapped_column(String(32), nullable=False)
	source_system: Mapped[str] = mapped_column(String(50), nullable=False)
	http_status: Mapped[Optional[int]] = mapped_column(Integer)
	correlation_id: Mapped[Optional[str]] = mapped_column(String(64))
	event_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	payload_json: Mapped[Optional[str]] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	vessel = relationship("Vessel", back_populates="api_events")


class VesselAdvice(Base):
	__tablename__ = "vessel_advice"

	vessel_advice_no: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	vessel_name: Mapped[str] = mapped_column(String(100), nullable=False)
	system_vessel_name: Mapped[str] = mapped_column(String(20), nullable=False)
	effective_start_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	effective_end_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class BerthApplication(Base):
	__tablename__ = "berth_application"

	application_no: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	vessel_advice_no: Mapped[int] = mapped_column(BigInteger, ForeignKey("vessel_advice.vessel_advice_no"), nullable=False)
	vessel_close_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime)
	deleted: Mapped[str] = mapped_column(String(1), nullable=False, default="N")
	berthing_status: Mapped[str] = mapped_column(String(1), nullable=False, default="A")
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

	vessel_advice = relationship("VesselAdvice")
