const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

let supabase;

if (supabaseUrl && supabaseKey) {
    try {
        supabase = createClient(supabaseUrl, supabaseKey);
        console.log("[Focus-Pocus] Connected to remote Supabase database.");
    } catch (e) {
        console.warn("[Focus-Pocus] Failed to initialize Supabase client:", e.message);
    }
}

if (!supabase) {
    console.warn(
        "\n[Focus-Pocus Backend] ⚠️ SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not configured in backend/.env."
    );
    console.warn(
        "[Focus-Pocus Backend] 💡 Running with in-memory development database for subjects and study sessions.\n"
    );

    // In-memory data store for local development without Supabase setup
    const memoryDb = {
        subjects: [
            { id: 1, user_id: process.env.PROTOTYPE_USER_ID || "demo-user", name: "Data Structures" },
            { id: 2, user_id: process.env.PROTOTYPE_USER_ID || "demo-user", name: "Mathematics" },
            { id: 3, user_id: process.env.PROTOTYPE_USER_ID || "demo-user", name: "Machine Learning" }
        ],
        study_sessions: [],
        nextSubjectId: 4,
        nextSessionId: 1
    };

    function createQuery(table) {
        let filters = [];
        let sortField = null;
        let isAscending = true;
        let pendingInsert = null;
        let pendingUpdate = null;
        let isDelete = false;

        const chain = {
            select(fields = "*") {
                return chain;
            },
            eq(col, val) {
                filters.push((item) => item[col] == val);
                return chain;
            },
            is(col, val) {
                filters.push((item) => item[col] === val);
                return chain;
            },
            not(col, op, val) {
                if (op === "is" && val === null) {
                    filters.push((item) => item[col] !== null && item[col] !== undefined);
                }
                return chain;
            },
            order(col, options = { ascending: true }) {
                sortField = col;
                isAscending = options?.ascending !== false;
                return chain;
            },
            insert(row) {
                pendingInsert = row;
                return chain;
            },
            update(fields) {
                pendingUpdate = fields;
                return chain;
            },
            delete() {
                isDelete = true;
                return chain;
            },
            async single() {
                const res = await chain.execute();
                if (res.error) return res;
                return { data: Array.isArray(res.data) ? res.data[0] || null : res.data, error: null };
            },
            async maybeSingle() {
                const res = await chain.execute();
                if (res.error) return res;
                return { data: Array.isArray(res.data) ? res.data[0] || null : res.data, error: null };
            },
            then(resolve, reject) {
                return chain.execute().then(resolve, reject);
            },
            async execute() {
                const list = memoryDb[table] || [];

                if (pendingInsert) {
                    const newRow = { ...pendingInsert };
                    if (table === "subjects") {
                        const exists = list.some(
                            s => s.user_id === newRow.user_id && s.name.toLowerCase() === newRow.name.toLowerCase()
                        );
                        if (exists) {
                            return { data: null, error: { code: "23505", message: "Duplicate subject" } };
                        }
                        newRow.id = memoryDb.nextSubjectId++;
                    } else if (table === "study_sessions") {
                        const active = list.some(
                            s => s.user_id === newRow.user_id && s.check_out === null
                        );
                        if (active) {
                            return { data: null, error: { code: "23505", message: "Active session exists" } };
                        }
                        newRow.id = memoryDb.nextSessionId++;
                        newRow.check_in = newRow.check_in || new Date().toISOString();
                        newRow.check_out = newRow.check_out || null;
                    }
                    list.push(newRow);
                    return { data: newRow, error: null };
                }

                if (isDelete) {
                    const idx = list.findIndex(item => filters.every(f => f(item)));
                    if (idx !== -1) {
                        const removed = list.splice(idx, 1)[0];
                        return { data: removed, error: null };
                    }
                    return { data: null, error: null };
                }

                if (pendingUpdate) {
                    const matched = list.find(item => filters.every(f => f(item)));
                    if (matched) {
                        Object.assign(matched, pendingUpdate);
                        return { data: matched, error: null };
                    }
                    return { data: null, error: null };
                }

                // Query
                let results = list.filter(item => filters.every(f => f(item)));
                if (sortField) {
                    results.sort((a, b) => {
                        if (a[sortField] < b[sortField]) return isAscending ? -1 : 1;
                        if (a[sortField] > b[sortField]) return isAscending ? 1 : -1;
                        return 0;
                    });
                }
                return { data: results, error: null };
            }
        };

        return chain;
    }

    supabase = {
        from(table) {
            return createQuery(table);
        }
    };
}

module.exports = supabase;
