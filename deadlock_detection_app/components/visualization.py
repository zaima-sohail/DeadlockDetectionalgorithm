import streamlit as st
import time


def to_lst(x):
    return x.tolist() if hasattr(x, 'tolist') else list(x)


def to_int_lst(x):
    return [int(i) for i in to_lst(x)]


def to_latex_matrix(lst):
    if len(lst) == 0:
        return "\\emptyset"

    # Check if 2D
    if hasattr(lst, "ndim") and lst.ndim == 2 or (
        len(lst) > 0 and (isinstance(lst[0], (list, tuple)) or hasattr(lst[0], 'tolist'))
    ):
        res = "\\begin{bmatrix}\n"
        for row in lst:
            res += " & ".join(map(str, to_int_lst(row))) + " \\\\\n"
        res += "\\end{bmatrix}"
        return res

    return "\\begin{bmatrix} " + " & ".join(map(str, to_int_lst(lst))) + " \\end{bmatrix}"


def render_dry_run(steps, algorithm_type="detection"):
    """
    Renders the dry run steps with detailed explanations and animations.
    """
    st.markdown(f"## 🏁 {algorithm_type.title()} Dry Run")

    if 'current_step_idx' not in st.session_state:
        st.session_state.current_step_idx = 0

    st.markdown("### 🎛️ Execution Controls")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("⏮️ Reset"):
            st.session_state.current_step_idx = 0
    with col2:
        if st.button("⏪ Previous"):
            st.session_state.current_step_idx = max(0, st.session_state.current_step_idx - 1)
    with col3:
        if st.button("Next ⏩"):
            st.session_state.current_step_idx = min(len(steps) - 1, st.session_state.current_step_idx + 1)
    with col4:
        if st.button("⏭️ End"):
            st.session_state.current_step_idx = len(steps) - 1

    progress = (st.session_state.current_step_idx + 1) / len(steps)
    st.progress(progress, text=f"Step {st.session_state.current_step_idx + 1} of {len(steps)}")

    step = steps[st.session_state.current_step_idx]

    # Display the current step
    render_step_card(step, algorithm_type)


def render_step_card(step, algorithm_type):
    st.markdown("---")

    if step['step_type'] == 'request_initial':
        # Dedicated rendering for Banker resource request initial snapshot
        st.info(f"### 🚀 Resource Request Start\n{step.get('details','')}")
        if step.get('explanation'):
            st.markdown(f"**Teacher's Note:** {step['explanation']}")

        process_id = step.get('process', step.get('process_id', ''))
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Request Vector**")
            if 'request' in step:
                st.latex(to_latex_matrix(to_lst(step['request'])))
        with c2:
            st.markdown("**Available Before**")
            if 'available_before' in step:
                st.latex(to_latex_matrix(to_lst(step['available_before'])))

        if 'need_for_process_before' in step:
            st.markdown("**Need (Max - Allocation) for Requesting Process Before**")
            st.latex(to_latex_matrix(to_lst(step['need_for_process_before'])))

    elif step['step_type'] == 'pretend_grant':
        st.info(f"### 🧮 Pretend Grant Update\n{step.get('details','')}")
        if step.get('explanation'):
            st.markdown(f"**Teacher's Note:** {step['explanation']}")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Available Before**")
            st.latex(to_latex_matrix(to_lst(step.get('available_before', []))))
        with c2:
            st.markdown("**Available After**")
            st.latex(to_latex_matrix(to_lst(step.get('available_after', []))))
        with c3:
            st.markdown("**Allocation Pⱼ Before/After**")
            before_a = step.get('allocation_before', [])
            after_a = step.get('allocation_after', [])
            st.latex(to_latex_matrix([before_a]))
            st.caption("before")
            st.latex(to_latex_matrix([after_a]))
            st.caption("after")

        if 'need_for_process_after' in step:
            st.markdown("**Need for Requesting Process After**")
            st.latex(to_latex_matrix(to_lst(step.get('need_for_process_after', []))))

    elif step['step_type'] == 'request_final':
        if step.get('granted'):
            st.success(f"### ✅ Request Granted\n{step.get('details','')}")
        else:
            st.error(f"### ⚠️ Request Denied\n{step.get('details','')}")

        if step.get('safe_sequence'):
            seq_str = " ➔ ".join([f"P{p}" for p in step.get('safe_sequence', [])])
            if step.get('granted'):
                st.markdown(f"**Safe Sequence:** `{seq_str}`")

        if 'available_after' in step:
            st.markdown("**Available After**")
            st.latex(to_latex_matrix(to_lst(step['available_after'])))

    elif step['step_type'] == 'initial':
        st.info(f"### 🚀 Initial State\n{step['details']}")
        st.markdown(f"**Teacher's Note:** {step['explanation']}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Initial Work Vector:**")
            st.latex(to_latex_matrix(to_lst(step['work'])))
        with c2:
            st.markdown("**Initial Finish Vector:**")
            st.latex(to_latex_matrix(to_int_lst(step['finish'])))

        if "banker" in algorithm_type and 'need' in step:
            with st.expander("📝 View Full Need Matrix (Max - Allocation)"):
                st.dataframe(step['need'], use_container_width=True)

    elif step['step_type'] in ['check', 'check_need', 'check_available']:
        status_passed = bool(step.get('condition_passed'))
        status_class = "step-success" if status_passed else "step-error"
        title = "✅ Request/Need OK" if status_passed else "⏳ Request Not Allowed"

        process_id = step.get('process', step.get('process_id', None))

        details = step.get('details', '')
        explanation = step.get('explanation', '')

        st.markdown(
            f"""
        <div class="glass-card {status_class}">
            <h3>{title}: P{process_id}</h3>
            <p>{details}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if explanation:
            st.markdown(f"**Expert Logic:** {explanation}")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Vector Comparison**")

            # Fix: Banker pre-check rendering so inequality always shows.
            if 'banker' in algorithm_type:
                if step['step_type'] == 'check_need':
                    req_val = step.get('request')
                    need_val = step.get('need_for_process')
                    st.markdown("**Inequality Shown:**")
                    if req_val is not None and need_val is not None:
                        st.latex(rf"\\text{{Request}}[P_{{{process_id}}}] \\le \\text{{Need}}[P_{{{process_id}}}]")
                        st.latex(rf"{to_latex_matrix(to_lst(req_val))} \\le {to_latex_matrix(to_lst(need_val))}")
                    else:
                        st.caption("(Request/Need values missing from step data)")

                elif step['step_type'] == 'check_available':
                    req_val = step.get('request')
                    avail_val = step.get('available_before')
                    st.markdown("**Inequality Shown:**")
                    if req_val is not None and avail_val is not None:
                        st.latex(r"\\text{Request} \\le \\text{Available}")
                        st.latex(rf"{to_latex_matrix(to_lst(req_val))} \\le {to_latex_matrix(to_lst(avail_val))}")
                    else:
                        st.caption("(Request/Available values missing from step data)")

                else:
                    # Safety-algorithm 'check' steps
                    st.caption("(Comparison data not available for this step)")
            else:
                st.caption("(Comparison data not available)")

            st.markdown(
                "<div style='text-align: center; color: #22C55E; font-weight: bold;'>✅ TRUE</div>"
                if status_passed
                else "<div style='text-align: center; color: #EF4444; font-weight: bold;'>❌ FALSE</div>",
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown("**Resources Released**")
            st.latex(r"\\emptyset")
            if status_passed:
                st.markdown(
                    "<div style='text-align: center; color: #22C55E;'>(Pre-check passed; proceed)</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div style='text-align: center; color: #F59E0B;'>(Request must wait/denied)</div>",
                    unsafe_allow_html=True,
                )

        with c3:
            st.markdown("**Updated Work**")
            st.latex(r"\\emptyset")
            st.markdown("<div style='text-align: center; color: #64748B;'>(Unchanged)</div>", unsafe_allow_html=True)

    elif step['step_type'] == 'check':
        # Existing (non-banker) check rendering
        status_class = "step-success" if step['condition_passed'] else "step-error"
        title = "✅ Process Executed" if step['condition_passed'] else "⏳ Process Waiting"

        st.markdown(
            f"""
        <div class="glass-card {status_class}">
            <h3>{title}: P{step['process']}</h3>
            <p>{step['details']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(f"**Expert Logic:** {step['explanation']}")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Vector Comparison**")
            req_label = "Need" if "banker" in algorithm_type else "Request"
            req_val = step['need_val'] if "banker" in algorithm_type else step['request']

            st.latex(rf"\\text{{{req_label}}}[P_{{{step['process']}}}] \\le \\text{{Work}}")
            st.latex(rf"{to_latex_matrix(to_lst(req_val))} \\le {to_latex_matrix(to_lst(step['work_before']))}")

            st.markdown(
                "<div style='text-align: center; color: #22C55E; font-weight: bold;'>✅ TRUE</div>"
                if step['condition_passed']
                else "<div style='text-align: center; color: #EF4444; font-weight: bold;'>❌ FALSE</div>",
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown("**Resources Released**")
            if step['condition_passed']:
                st.latex(f"+ {to_latex_matrix(to_lst(step['allocation_released']))}")
                st.markdown("<div style='text-align: center; color: #22C55E;'>(Added to Work)</div>", unsafe_allow_html=True)
            else:
                st.latex(r"\\emptyset")
                st.markdown("<div style='text-align: center; color: #F59E0B;'>(Process must wait)</div>", unsafe_allow_html=True)

        with c3:
            st.markdown("**Updated Work**")
            work_after = step['work_after'] if step['condition_passed'] else step['work_before']
            st.latex(to_latex_matrix(to_lst(work_after)))
            st.markdown(
                "<div style='text-align: center; color: #22C55E;'>(Updated)</div>"
                if step['condition_passed']
                else "<div style='text-align: center; color: #64748B;'>(Unchanged)</div>",
                unsafe_allow_html=True,
            )

    elif step['step_type'] == 'final':
        if algorithm_type == "detection":
            if step['is_deadlocked']:
                dead_str = ", ".join([f"P{p}" for p in step['deadlocked_processes']])
                st.error(f"### 💥 Deadlock Detected!\n**Processes involved:** `{dead_str}`")
            else:
                seq_str = " ➔ ".join([f"P{p}" for p in step['safe_sequence']])
                st.success(f"### ✅ System is Safe!\nNo deadlocks found. **Safe Sequence:** `{seq_str}`")
        else:
            if step['is_safe']:
                seq_str = " ➔ ".join([f"P{p}" for p in step['safe_sequence']])
                st.success(f"### ✅ System is Safe!\n**Safe Sequence:** `{seq_str}`")
            else:
                st.error("### ⚠️ System is UNSAFE!\nNo safe sequence exists.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Final Work Vector:**")
            st.latex(to_latex_matrix(to_lst(step['work'])))
        with c2:
            st.markdown("**Final Finish Array:**")
            st.latex(to_latex_matrix(to_int_lst(step['finish'])))

