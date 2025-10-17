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


async def seed_containers(session: AsyncSession) -> None:
	"""Seed all 20 containers from SQL"""
	containers = [
		Container(cntr_no='MSKU0000001', iso_code='22G1', size_type='20GP', gross_weight_kg=12000, status='TRANSHIP', origin_port='CNSHA', tranship_port='SGSIN', destination_port='MYTPP', vessel_id=1, eta_ts=datetime(2025, 10, 4, 12, 0), etd_ts=datetime(2025, 10, 5, 18, 0), last_free_day=datetime(2025, 10, 10).date()),
		Container(cntr_no='MSKU0000002', iso_code='45R1', size_type='40RF', gross_weight_kg=8000, status='IN_YARD', origin_port='HKHKG', tranship_port='SGSIN', destination_port='IDJKT', vessel_id=2, eta_ts=datetime(2025, 10, 5, 8, 0), etd_ts=datetime(2025, 10, 6, 20, 0), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='MSKU0000003', iso_code='22G1', size_type='20GP', gross_weight_kg=11000, status='DISCHARGED', origin_port='CNSZX', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=3, eta_ts=datetime(2025, 10, 3, 16, 0), etd_ts=None, last_free_day=datetime(2025, 10, 9).date()),
		Container(cntr_no='MSKU0000004', iso_code='22G1', size_type='20GP', gross_weight_kg=13000, status='LOADED', origin_port='MYTPP', tranship_port='SGSIN', destination_port='JPTYO', vessel_id=4, eta_ts=datetime(2025, 10, 6, 10, 0), etd_ts=datetime(2025, 10, 6, 22, 0), last_free_day=datetime(2025, 10, 12).date()),
		Container(cntr_no='MSKU0000005', iso_code='45G1', size_type='40HQ', gross_weight_kg=15000, status='TRANSHIP', origin_port='JPTYO', tranship_port='SGSIN', destination_port='CNSHA', vessel_id=5, eta_ts=datetime(2025, 10, 4, 18, 0), etd_ts=datetime(2025, 10, 5, 23, 0), last_free_day=datetime(2025, 10, 10).date()),
		Container(cntr_no='MSCU0000006', iso_code='45G1', size_type='40HQ', gross_weight_kg=14500, status='IN_YARD', origin_port='SGSIN', tranship_port='SGSIN', destination_port='USLAX', vessel_id=6, eta_ts=datetime(2025, 10, 7, 6, 0), etd_ts=datetime(2025, 10, 8, 2, 0), last_free_day=datetime(2025, 10, 13).date()),
		Container(cntr_no='MSCU0000007', iso_code='22G1', size_type='20GP', gross_weight_kg=10000, status='TRANSHIP', origin_port='CNSHA', tranship_port='SGSIN', destination_port='HKHKG', vessel_id=7, eta_ts=datetime(2025, 10, 5, 5, 0), etd_ts=datetime(2025, 10, 5, 20, 0), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='MSCU0000008', iso_code='22G1', size_type='20GP', gross_weight_kg=11500, status='GATE_IN', origin_port='HKHKG', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=8, eta_ts=datetime(2025, 10, 4, 9, 0), etd_ts=None, last_free_day=datetime(2025, 10, 9).date()),
		Container(cntr_no='MSCU0000009', iso_code='22G1', size_type='20GP', gross_weight_kg=12500, status='ON_VESSEL', origin_port='SGSIN', tranship_port='SGSIN', destination_port='CAXMN', vessel_id=9, eta_ts=None, etd_ts=datetime(2025, 10, 6, 12, 0), last_free_day=datetime(2025, 10, 12).date()),
		Container(cntr_no='MSCU0000010', iso_code='45R1', size_type='40RF', gross_weight_kg=9000, status='TRANSHIP', origin_port='CAXMN', tranship_port='SGSIN', destination_port='SGSIN', hazard_class='9', vessel_id=10, eta_ts=datetime(2025, 10, 5, 14, 0), etd_ts=datetime(2025, 10, 6, 14, 0), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='OOLU0000011', iso_code='45G1', size_type='40HQ', gross_weight_kg=14800, status='TRANSHIP', origin_port='KRPTK', tranship_port='SGSIN', destination_port='AEMAA', vessel_id=1, eta_ts=datetime(2025, 10, 6, 2, 0), etd_ts=datetime(2025, 10, 7, 1, 0), last_free_day=datetime(2025, 10, 13).date()),
		Container(cntr_no='OOLU0000012', iso_code='22G1', size_type='20GP', gross_weight_kg=10800, status='DISCHARGED', origin_port='AEMAA', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=2, eta_ts=datetime(2025, 10, 3, 22, 0), etd_ts=None, last_free_day=datetime(2025, 10, 9).date()),
		Container(cntr_no='OOLU0000013', iso_code='22G1', size_type='20GP', gross_weight_kg=11800, status='LOADED', origin_port='SGSIN', tranship_port='SGSIN', destination_port='INNSA', vessel_id=3, eta_ts=None, etd_ts=datetime(2025, 10, 5, 21, 0), last_free_day=datetime(2025, 10, 12).date()),
		Container(cntr_no='OOLU0000014', iso_code='22G1', size_type='20GP', gross_weight_kg=11200, status='GATE_OUT', origin_port='SGSIN', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=4, eta_ts=None, etd_ts=None, last_free_day=datetime(2025, 10, 8).date()),
		Container(cntr_no='TEMU0000015', iso_code='45G1', size_type='40HQ', gross_weight_kg=15100, status='TRANSHIP', origin_port='INNSA', tranship_port='SGSIN', destination_port='CNSHA', vessel_id=5, eta_ts=datetime(2025, 10, 4, 20, 0), etd_ts=datetime(2025, 10, 6, 0, 0), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='TEMU0000016', iso_code='45R1', size_type='40RF', gross_weight_kg=8600, status='IN_YARD', origin_port='CNSHA', tranship_port='SGSIN', destination_port='MYTPP', hazard_class='3', vessel_id=6, eta_ts=datetime(2025, 10, 7, 8, 0), etd_ts=datetime(2025, 10, 8, 3, 0), last_free_day=datetime(2025, 10, 13).date()),
		Container(cntr_no='TEMU0000017', iso_code='22G1', size_type='20GP', gross_weight_kg=12200, status='TRANSHIP', origin_port='HKHKG', tranship_port='SGSIN', destination_port='JPTYO', vessel_id=7, eta_ts=datetime(2025, 10, 5, 11, 0), etd_ts=datetime(2025, 10, 5, 23, 59), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='TEMU0000018', iso_code='22G1', size_type='20GP', gross_weight_kg=11900, status='ON_VESSEL', origin_port='JPTYO', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=8, eta_ts=None, etd_ts=datetime(2025, 10, 6, 3, 0), last_free_day=datetime(2025, 10, 12).date()),
		Container(cntr_no='CMAU0000019', iso_code='45G1', size_type='40HQ', gross_weight_kg=14950, status='TRANSHIP', origin_port='USLAX', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=9, eta_ts=datetime(2025, 10, 5, 16, 0), etd_ts=datetime(2025, 10, 6, 18, 0), last_free_day=datetime(2025, 10, 11).date()),
		Container(cntr_no='CMAU0000020', iso_code='22G1', size_type='20GP', gross_weight_kg=10990, status='DISCHARGED', origin_port='CAXMN', tranship_port='SGSIN', destination_port='SGSIN', vessel_id=10, eta_ts=datetime(2025, 10, 3, 13, 0), etd_ts=None, last_free_day=datetime(2025, 10, 9).date()),
	]
	session.add_all(containers)
	await session.flush()


async def seed_edi_messages(session: AsyncSession) -> None:
	"""Seed all 20 EDI messages from SQL"""
	edi_messages = [
		EdiMessage(container_id=1, vessel_id=1, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0001', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 3, 8, 1), ack_at=datetime(2025, 10, 3, 8, 2), raw_text='UNA:+.? \nUNB+...'),
		EdiMessage(container_id=2, vessel_id=2, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0002', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 3, 8, 5), ack_at=datetime(2025, 10, 3, 8, 6), raw_text='UNA:+.? \nUNB+...'),
		EdiMessage(container_id=3, vessel_id=3, message_type='COARRI', direction='OUT', status='ACKED', message_ref='REF-ARR-0003', sender='PSA-TOS', receiver='LINE-PSA', sent_at=datetime(2025, 10, 3, 17, 10), ack_at=datetime(2025, 10, 3, 17, 12), raw_text='UNH+...'),
		EdiMessage(container_id=4, vessel_id=4, message_type='COARRI', direction='OUT', status='ACKED', message_ref='REF-ARR-0004', sender='PSA-TOS', receiver='LINE-PSA', sent_at=datetime(2025, 10, 4, 6, 40), ack_at=datetime(2025, 10, 4, 6, 41), raw_text='UNH+...'),
		EdiMessage(container_id=5, vessel_id=5, message_type='CODECO', direction='OUT', status='ACKED', message_ref='REF-DEC-0005', sender='PSA-DEPOT', receiver='LINE-PSA', sent_at=datetime(2025, 10, 4, 9, 0), ack_at=datetime(2025, 10, 4, 9, 1), raw_text='UNH+...'),
		EdiMessage(container_id=6, vessel_id=6, message_type='IFTMIN', direction='IN', status='PARSED', message_ref='REF-IFT-0006', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 4, 12, 20), ack_at=datetime(2025, 10, 4, 12, 21), raw_text='UNH+...'),
		EdiMessage(container_id=7, vessel_id=7, message_type='IFTMIN', direction='IN', status='ERROR', message_ref='REF-IFT-0007', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 4, 12, 25), ack_at=None, error_text='Segment missing', raw_text='UNH+...'),
		EdiMessage(container_id=8, vessel_id=8, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0008', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 4, 13, 10), ack_at=datetime(2025, 10, 4, 13, 11), raw_text='UNH+...'),
		EdiMessage(container_id=9, vessel_id=9, message_type='COARRI', direction='OUT', status='ACKED', message_ref='REF-ARR-0009', sender='PSA-TOS', receiver='LINE-PSA', sent_at=datetime(2025, 10, 4, 14, 33), ack_at=datetime(2025, 10, 4, 14, 34), raw_text='UNH+...'),
		EdiMessage(container_id=10, vessel_id=10, message_type='CODECO', direction='OUT', status='ACKED', message_ref='REF-DEC-0010', sender='PSA-DEPOT', receiver='LINE-PSA', sent_at=datetime(2025, 10, 4, 15, 0), ack_at=datetime(2025, 10, 4, 15, 2), raw_text='UNH+...'),
		EdiMessage(container_id=11, vessel_id=1, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0011', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 7, 5), ack_at=datetime(2025, 10, 5, 7, 6), raw_text='UNH+...'),
		EdiMessage(container_id=12, vessel_id=2, message_type='IFTMIN', direction='IN', status='PARSED', message_ref='REF-IFT-0012', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 7, 15), ack_at=datetime(2025, 10, 5, 7, 16), raw_text='UNH+...'),
		EdiMessage(container_id=13, vessel_id=3, message_type='COARRI', direction='OUT', status='ACKED', message_ref='REF-ARR-0013', sender='PSA-TOS', receiver='LINE-PSA', sent_at=datetime(2025, 10, 5, 8, 20), ack_at=datetime(2025, 10, 5, 8, 21), raw_text='UNH+...'),
		EdiMessage(container_id=14, vessel_id=4, message_type='CODECO', direction='OUT', status='ACKED', message_ref='REF-DEC-0014', sender='PSA-DEPOT', receiver='LINE-PSA', sent_at=datetime(2025, 10, 5, 9, 20), ack_at=datetime(2025, 10, 5, 9, 22), raw_text='UNH+...'),
		EdiMessage(container_id=15, vessel_id=5, message_type='IFTMIN', direction='IN', status='PARSED', message_ref='REF-IFT-0015', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 10, 10), ack_at=datetime(2025, 10, 5, 10, 11), raw_text='UNH+...'),
		EdiMessage(container_id=16, vessel_id=6, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0016', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 10, 30), ack_at=datetime(2025, 10, 5, 10, 31), raw_text='UNH+...'),
		EdiMessage(container_id=17, vessel_id=7, message_type='COARRI', direction='OUT', status='ACKED', message_ref='REF-ARR-0017', sender='PSA-TOS', receiver='LINE-PSA', sent_at=datetime(2025, 10, 5, 11, 0), ack_at=datetime(2025, 10, 5, 11, 2), raw_text='UNH+...'),
		EdiMessage(container_id=18, vessel_id=8, message_type='CODECO', direction='OUT', status='ACKED', message_ref='REF-DEC-0018', sender='PSA-DEPOT', receiver='LINE-PSA', sent_at=datetime(2025, 10, 5, 12, 0), ack_at=datetime(2025, 10, 5, 12, 1), raw_text='UNH+...'),
		EdiMessage(container_id=19, vessel_id=9, message_type='IFTMIN', direction='IN', status='PARSED', message_ref='REF-IFT-0019', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 12, 30), ack_at=datetime(2025, 10, 5, 12, 31), raw_text='UNH+...'),
		EdiMessage(container_id=20, vessel_id=10, message_type='COPARN', direction='IN', status='PARSED', message_ref='REF-COP-0020', sender='LINE-PSA', receiver='PSA-TOS', sent_at=datetime(2025, 10, 5, 13, 0), ack_at=datetime(2025, 10, 5, 13, 2), raw_text='UNH+...'),
	]
	session.add_all(edi_messages)
	await session.flush()


async def seed_api_events(session: AsyncSession) -> None:
	"""Seed all 20 API events from SQL"""
	api_events = [
		ApiEvent(container_id=1, vessel_id=1, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0001', event_ts=datetime(2025, 10, 3, 17, 20), payload_json='{"bay":"12","row":"04","tier":"06"}'),
		ApiEvent(container_id=2, vessel_id=2, event_type='GATE_IN', source_system='CMS', http_status=201, correlation_id='corr-0002', event_ts=datetime(2025, 10, 3, 18, 5), payload_json='{"gate":"C3"}'),
		ApiEvent(container_id=3, vessel_id=3, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0003', event_ts=datetime(2025, 10, 3, 18, 30), payload_json='{"crane":"QC-05"}'),
		ApiEvent(container_id=4, vessel_id=4, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0004', event_ts=datetime(2025, 10, 4, 6, 55), payload_json='{"stow":"23-08-04"}'),
		ApiEvent(container_id=5, vessel_id=5, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0005', event_ts=datetime(2025, 10, 4, 23, 10), payload_json='{"stow":"25-02-02"}'),
		ApiEvent(container_id=6, vessel_id=6, event_type='GATE_IN', source_system='CMS', http_status=200, correlation_id='corr-0006', event_ts=datetime(2025, 10, 5, 1, 15), payload_json='{"truck":"SGL1234Z"}'),
		ApiEvent(container_id=7, vessel_id=7, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0007', event_ts=datetime(2025, 10, 5, 5, 25), payload_json='{"stow":"11-06-07"}'),
		ApiEvent(container_id=8, vessel_id=8, event_type='GATE_OUT', source_system='CMS', http_status=200, correlation_id='corr-0008', event_ts=datetime(2025, 10, 5, 8, 40), payload_json='{"gate":"A1"}'),
		ApiEvent(container_id=9, vessel_id=9, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0009', event_ts=datetime(2025, 10, 5, 12, 5), payload_json='{"stow":"07-10-03"}'),
		ApiEvent(container_id=10, vessel_id=10, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0010', event_ts=datetime(2025, 10, 5, 14, 20), payload_json='{"crane":"QC-02"}'),
		ApiEvent(container_id=11, vessel_id=1, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0011', event_ts=datetime(2025, 10, 6, 1, 5), payload_json='{"stow":"18-04-01"}'),
		ApiEvent(container_id=12, vessel_id=2, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0012', event_ts=datetime(2025, 10, 6, 2, 30), payload_json='{"crane":"QC-07"}'),
		ApiEvent(container_id=13, vessel_id=3, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0013', event_ts=datetime(2025, 10, 6, 3, 10), payload_json='{"stow":"15-12-06"}'),
		ApiEvent(container_id=14, vessel_id=4, event_type='GATE_OUT', source_system='CMS', http_status=200, correlation_id='corr-0014', event_ts=datetime(2025, 10, 6, 4, 0), payload_json='{"truck":"SGK5678A"}'),
		ApiEvent(container_id=15, vessel_id=5, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0015', event_ts=datetime(2025, 10, 6, 5, 45), payload_json='{"stow":"09-03-09"}'),
		ApiEvent(container_id=16, vessel_id=6, event_type='GATE_IN', source_system='CMS', http_status=200, correlation_id='corr-0016', event_ts=datetime(2025, 10, 6, 7, 5), payload_json='{"gate":"B2"}'),
		ApiEvent(container_id=17, vessel_id=7, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0017', event_ts=datetime(2025, 10, 6, 9, 20), payload_json='{"stow":"03-01-02"}'),
		ApiEvent(container_id=18, vessel_id=8, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0018', event_ts=datetime(2025, 10, 6, 12, 15), payload_json='{"crane":"QC-03"}'),
		ApiEvent(container_id=19, vessel_id=9, event_type='LOAD', source_system='TOS', http_status=200, correlation_id='corr-0019', event_ts=datetime(2025, 10, 6, 15, 40), payload_json='{"stow":"05-08-10"}'),
		ApiEvent(container_id=20, vessel_id=10, event_type='DISCHARGE', source_system='TOS', http_status=200, correlation_id='corr-0020', event_ts=datetime(2025, 10, 6, 16, 55), payload_json='{"crane":"QC-09"}'),
	]
	session.add_all(api_events)
	await session.flush()


async def seed_vessel_advice(session: AsyncSession) -> None:
	"""Seed all vessel advice entries from SQL"""
	vessel_advice_entries = [
		VesselAdvice(vessel_advice_no=1000010960, vessel_name='MV Lion City 07', system_vessel_name='MV Lion City 07', effective_start_datetime=datetime(2025, 10, 1, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010500, vessel_name='MV Lion City 08', system_vessel_name='MV Lion City 08', effective_start_datetime=datetime(2025, 9, 15, 0, 0), effective_end_datetime=datetime(2025, 10, 1, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010961, vessel_name='MV Lion City 08', system_vessel_name='MV Lion City 08', effective_start_datetime=datetime(2025, 10, 1, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010962, vessel_name='MV Merlion 11', system_vessel_name='MV Merlion 11', effective_start_datetime=datetime(2025, 10, 2, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010400, vessel_name='MV Merlion 12', system_vessel_name='MV Merlion 12', effective_start_datetime=datetime(2025, 8, 1, 0, 0), effective_end_datetime=datetime(2025, 9, 1, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010600, vessel_name='MV Merlion 12', system_vessel_name='MV Merlion 12', effective_start_datetime=datetime(2025, 9, 5, 0, 0), effective_end_datetime=datetime(2025, 9, 20, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010700, vessel_name='MV Merlion 15', system_vessel_name='MV Merlion 15', effective_start_datetime=datetime(2025, 9, 10, 0, 0), effective_end_datetime=datetime(2025, 9, 25, 0, 0)),
		VesselAdvice(vessel_advice_no=1000010963, vessel_name='MV Merlion 15', system_vessel_name='MV Merlion 15', effective_start_datetime=datetime(2025, 9, 25, 0, 0)),
	]
	session.add_all(vessel_advice_entries)
	await session.flush()


async def seed_berth_applications(session: AsyncSession) -> None:
	"""Seed all berth applications from SQL"""
	berth_applications = [
		BerthApplication(vessel_advice_no=1000010960, deleted='N', berthing_status='A'),
		BerthApplication(vessel_advice_no=1000010961, deleted='N', berthing_status='A'),
		BerthApplication(vessel_advice_no=1000010962, deleted='N', berthing_status='A'),
		BerthApplication(vessel_advice_no=1000010963, deleted='N', berthing_status='A'),
	]
	session.add_all(berth_applications)
	await session.flush()


async def seed_extras(session: AsyncSession) -> None:
	"""Seed all additional data beyond vessels"""
	await seed_containers(session)
	await seed_edi_messages(session)
	await seed_api_events(session)
	await seed_vessel_advice(session)
	await seed_berth_applications(session)
