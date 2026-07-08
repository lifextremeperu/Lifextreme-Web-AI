/**
 * Store de Mochila Táctica (Atomic State Management - Vanilla JS)
 * Implementa un patrón de suscripción para reactividad sin frameworks.
 */

const createStore = (initialState) => {
    let state = initialState;
    const listeners = new Set();

    const getState = () => state;

    const setState = (nextState) => {
        state = typeof nextState === 'function' ? nextState(state) : nextState;
        listeners.forEach(listener => listener(state));
    };

    const subscribe = (listener) => {
        listeners.add(listener);
        return () => listeners.delete(listener);
    };

    return { getState, setState, subscribe };
};

// --- INITIAL STATE ---
const initialState = {
    items: JSON.parse(localStorage.getItem('lifextreme_backpack')) || [],
    isOpen: false,
    lastAddedId: null,
    total: 0,
    membership: {
        startTime: parseInt(localStorage.getItem('lifextreme_membership_start')) || null,
        ttl: 24 * 60 * 60 * 1000, // 24 hours in ms
        isActive: localStorage.getItem('lifextreme_membership_start') !== null
    },
    draftBooking: JSON.parse(localStorage.getItem('lifextreme_draft_booking')) || {
        step: 1,
        tourId: null,
        participants: 1,
        selectedDay: null,
        selectedAddons: [],
        completed: false
    }
};

const store = createStore(initialState);

// --- BACKPACK HOOK (Vanilla Pattern) ---
const useBackpack = () => {
    const { getState, setState, subscribe } = store;

    const calculateTotal = (items) => items.reduce((acc, item) => acc + item.price, 0);

    const addItem = (item) => {
        setState(state => {
            const newItems = [...state.items, { ...item, timestamp: Date.now() }];
            localStorage.setItem('lifextreme_backpack', JSON.stringify(newItems));
            return {
                ...state,
                items: newItems,
                lastAddedId: item.id || Date.now(),
                total: calculateTotal(newItems)
            };
        });
        // Trigger visual feedback (vibration/fly-to-bag)
        document.dispatchEvent(new CustomEvent('backpack-item-added', { detail: item }));
    };

    const removeItem = (index) => {
        setState(state => {
            const newItems = state.items.filter((_, i) => i !== index);
            localStorage.setItem('lifextreme_backpack', JSON.stringify(newItems));
            return {
                ...state,
                items: newItems,
                total: calculateTotal(newItems)
            };
        });
    };

    const toggleOpen = () => {
        setState(state => ({ ...state, isOpen: !state.isOpen }));
    };

    return {
        getState,
        subscribe,
        addItem,
        removeItem,
        toggleOpen
    };
};

// --- MEMBERSHIP HOOK (Loss Aversion Logic) ---
const useMembership = () => {
    const { getState, setState, subscribe } = store;

    const initMembership = () => {
        const now = Date.now();
        localStorage.setItem('lifextreme_membership_start', now.toString());
        setState(state => ({
            ...state,
            membership: { ...state.membership, startTime: now, isActive: true }
        }));
    };

    const getRemainingTime = () => {
        const { membership } = getState();
        if (!membership.startTime) return 0;
        const elapsed = Date.now() - membership.startTime;
        return Math.max(0, membership.ttl - elapsed);
    };

    const calculateLostSavings = () => {
        const { total } = getState();
        return Math.round(total * 0.15); // The 15% they are "losing"
    };

    return {
        getState,
        subscribe,
        initMembership,
        getRemainingTime,
        calculateLostSavings
    };
};

// --- DRAFT BOOKING HOOK (Wizard Persistence) ---
const useDraftBooking = () => {
    const { getState, setState, subscribe } = store;

    const updateDraft = (data) => {
        setState(state => {
            const newDraft = { ...state.draftBooking, ...data };
            localStorage.setItem('lifextreme_draft_booking', JSON.stringify(newDraft));
            return { ...state, draftBooking: newDraft };
        });
    };

    const clearDraft = () => {
        localStorage.removeItem('lifextreme_draft_booking');
        setState(state => ({
            ...state,
            draftBooking: { step: 1, tourId: null, participants: 1, selectedDay: null, selectedAddons: [], completed: false }
        }));
    };

    return { getState, subscribe, updateDraft, clearDraft };
};

// Exportar para uso global
window.useBackpack = useBackpack;
window.useMembership = useMembership;
window.useDraftBooking = useDraftBooking;
