/**
 * Tipado Fuerte TypeScript para la Telemetría Ferroviaria Simulada (PeruRail / Inca Rail)
 * en el Centro de Comando Geoespacial 3D (lifextreme.store/geoint).
 */

import type { Feature, LineString, Point } from 'geojson';

export type TrainOperator = 'PeruRail' | 'Inca Rail';

export type TrainStatus = 'en_ruta' | 'en_estacion' | 'programado';

export type TrainRouteSegmentId =
    | 'SanPedro_Ollantaytambo'
    | 'Poroy_AguasCalientes'
    | 'Ollantaytambo_AguasCalientes'
    | 'AguasCalientes_Ollantaytambo'
    | 'AguasCalientes_Hidroelectrica';

export interface TrainEndpointTimestamp {
    station: string;
    timestamp_ms: number;
}

export interface TrainTelemetryPayload {
    train_id: string;
    operator: TrainOperator;
    service?: string;
    status: TrainStatus;
    route_segment: TrainRouteSegmentId;
    speed_kmh?: number;
    wagons?: number;
    occupancy_pct?: number;
    departure: TrainEndpointTimestamp;
    arrival: TrainEndpointTimestamp;
}

export interface CachedRailwaySegment {
    segmentId: TrainRouteSegmentId;
    lineFeature: Feature<LineString>;
    totalDistanceKm: number;
}

export interface InterpolatedTrainState {
    payload: TrainTelemetryPayload;
    longitude: number;
    latitude: number;
    elevation: number;
    bearingDeg: number;
    progressPct: number;
    distanceTraveledKm: number;
    totalDistanceKm: number;
    etaMinutes: number;
    etaFormatted: string;
}
