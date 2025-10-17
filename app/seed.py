from __future__ import annotations

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Vessel, Container, EdiMessage, ApiEvent, VesselAdvice, BerthApplication


async def seed_vessels(session: AsyncSession) -> None:
	vessels = [
		Vessel(imo_no=9300001, vessel_name='MV Lion City 01', call_sign='9VLC1', operator_name='Oceanic Shipping', flag_state='Singapore', built_year=2010, capacity_teu=14000, loa_m=366.00, beam_m=51.00, draft_m=15.00, last_port='CNSHA', next_port='SGSIN'),
		Vessel(imo_no=9300002, vessel_name='MV Lion City 02', call_sign='9VLC2', operator_name='BlueWave Lines', flag_state='Panama', built_year=2011, capacity_teu=14500, loa_m=368.50, beam_m=51.20, draft_m=15.20, last_port='HKHKG', next_port='CNSHA'),
		Vessel(imo_no=9300003, vessel_name='MV Lion City 03', call_sign='9VLC3', operator_name='HarborStar', flag_state='Liberia', built_year=2012, capacity_teu=15000, loa_m=370.00, beam_m=52.00, draft_m=15.50, last_port='SGSIN', next_port='MYTPP'),
		Vessel(imo_no=9300004, vessel_name='MV Lion City 04', call_sign='9VLC4', operator_name='Oceanic Shipping', flag_state='Marshall Islands', built_year=2013, capacity_teu=15500, loa_m=372.00, beam_m=52.10, draft_m=15.60, last_port='JPTYO', next_port='SGSIN'),
		Vessel(imo_no=9300005, vessel_name='MV Lion City 05', call_sign='9VLC5', operator_name='BlueWave Lines', flag_state='Denmark', built_year=2014, capacity_teu=16000, loa_m=375.00, beam_m=53.00, draft_m=15.80, last_port='SGSIN', next_port='HKHKG'),
		Vessel(imo_no=9300006, vessel_name='MV Lion City 06', call_sign='9VLC6', operator_name='HarborStar', flag_state='Malta', built_year=2015, capacity_teu=16500, loa_m=377.00, beam_m=53.50, draft_m=16.00, last_port='CNSZX', next_port='CNSHA'),
		Vessel(imo_no=9300007, vessel_name='MV Lion City 07', call_sign='9VLC7', operator_name='Trident Global', flag_state='Hong Kong', built_year=2016, capacity_teu=17000, loa_m=380.00, beam_m=54.00, draft_m=16.00, last_port='SGSIN', next_port='IDJKT'),
		Vessel(imo_no=9300008, vessel_name='MV Lion City 08', call_sign='9VLC8', operator_name='Oceanic Shipping', flag_state='Singapore', built_year=2017, capacity_teu=17500, loa_m=382.00, beam_m=54.20, draft_m=16.20, last_port='MYTPP', next_port='SGSIN'),
		Vessel(imo_no=9300009, vessel_name='MV Lion City 09', call_sign='9VLC9', operator_name='BlueWave Lines', flag_state='Germany', built_year=2018, capacity_teu=18000, loa_m=384.00, beam_m=55.00, draft_m=16.50, last_port='SGSIN', next_port='JPTYO'),
		Vessel(imo_no=9300010, vessel_name='MV Lion City 10', call_sign='9VLA0', operator_name='HarborStar', flag_state='UK', built_year=2019, capacity_teu=18500, loa_m=386.00, beam_m=55.10, draft_m=16.50, last_port='KRPTK', next_port='SGSIN'),
		Vessel(imo_no=9300011, vessel_name='MV Merlion 11', call_sign='9VML1', operator_name='Trident Global', flag_state='Singapore', built_year=2020, capacity_teu=19000, loa_m=388.00, beam_m=56.00, draft_m=16.50, last_port='SGSIN', next_port='HKHKG'),
		Vessel(imo_no=9300012, vessel_name='MV Merlion 12', call_sign='9VML2', operator_name='Oceanic Shipping', flag_state='Panama', built_year=2020, capacity_teu=19000, loa_m=388.00, beam_m=56.00, draft_m=16.50, last_port='HKHKG', next_port='SGSIN'),
		Vessel(imo_no=9300013, vessel_name='MV Merlion 13', call_sign='9VML3', operator_name='BlueWave Lines', flag_state='Liberia', built_year=2021, capacity_teu=19500, loa_m=390.00, beam_m=56.50, draft_m=16.60, last_port='CNSHA', next_port='SGSIN'),
		Vessel(imo_no=9300014, vessel_name='MV Merlion 14', call_sign='9VML4', operator_name='HarborStar', flag_state='Marshall Islands', built_year=2021, capacity_teu=19500, loa_m=390.00, beam_m=56.50, draft_m=16.60, last_port='SGSIN', next_port='CAXMN'),
		Vessel(imo_no=9300015, vessel_name='MV Merlion 15', call_sign='9VML5', operator_name='Trident Global', flag_state='Denmark', built_year=2022, capacity_teu=20000, loa_m=395.00, beam_m=57.00, draft_m=16.80, last_port='SGSIN', next_port='USLAX'),
		Vessel(imo_no=9300016, vessel_name='MV Merlion 16', call_sign='9VML6', operator_name='Oceanic Shipping', flag_state='Malta', built_year=2022, capacity_teu=20000, loa_m=395.00, beam_m=57.00, draft_m=16.80, last_port='USLAX', next_port='SGSIN'),
		Vessel(imo_no=9300017, vessel_name='MV Merlion 17', call_sign='9VML7', operator_name='BlueWave Lines', flag_state='Hong Kong', built_year=2023, capacity_teu=20500, loa_m=398.00, beam_m=58.00, draft_m=17.00, last_port='SGSIN', next_port='AEMAA'),
		Vessel(imo_no=9300018, vessel_name='MV Merlion 18', call_sign='9VML8', operator_name='HarborStar', flag_state='Singapore', built_year=2023, capacity_teu=20500, loa_m=398.00, beam_m=58.00, draft_m=17.00, last_port='AEMAA', next_port='SGSIN'),
		Vessel(imo_no=9300019, vessel_name='MV Merlion 19', call_sign='9VML9', operator_name='Trident Global', flag_state='Germany', built_year=2024, capacity_teu=21000, loa_m=400.00, beam_m=58.60, draft_m=17.20, last_port='SGSIN', next_port='INNSA'),
		Vessel(imo_no=9300020, vessel_name='MV Merlion 20', call_sign='9VMA0', operator_name='Oceanic Shipping', flag_state='Liberia', built_year=2024, capacity_teu=21000, loa_m=400.00, beam_m=58.60, draft_m=17.20, last_port='INNSA', next_port='SGSIN'),
	]
	session.add_all(vessels)
	await session.flush()


async def seed_extras(session: AsyncSession) -> None:
	# Minimal subset for demo; you can extend similarly using data from SQL
	container = Container(
		cntr_no='MSKU0000001', iso_code='22G1', size_type='20GP', gross_weight_kg=12000,
		status='TRANSHIP', origin_port='CNSHA', tranship_port='SGSIN', destination_port='MYTPP',
		vessel_id=1, eta_ts=datetime(2025, 10, 4, 12, 0), etd_ts=datetime(2025, 10, 5, 18, 0), last_free_day=datetime(2025, 10, 10).date(),
	)
	session.add(container)
	await session.flush()

	edi = EdiMessage(
		container_id=container.container_id, vessel_id=1, message_type='COPARN', direction='IN', status='PARSED',
		message_ref='REF-COP-0001', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 3, 8, 1), ack_at=datetime(2025, 10, 3, 8, 2), raw_text='UNA:+.? \nUNB+...'
	)
	session.add(edi)

	api_event = ApiEvent(
		container_id=container.container_id, vessel_id=1, event_type='DISCHARGE', source_system='TOS', http_status=200,
		correlation_id='corr-0001', event_ts=datetime(2025, 10, 3, 17, 20), payload_json='{"bay":"12","row":"04","tier":"06"}'
	)
	session.add(api_event)

	advice = VesselAdvice(
		vessel_advice_no=1000010960, vessel_name='MV Lion City 07', system_vessel_name='MV Lion City 07', effective_start_datetime=datetime(2025,10,1,0,0)
	)
	session.add(advice)
	await session.flush()

	ba = BerthApplication(vessel_advice_no=1000010960, deleted='N', berthing_status='A')
	session.add(ba)
