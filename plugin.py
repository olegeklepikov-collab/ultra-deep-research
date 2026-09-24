"""Public Hermes plugin entry point."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

try:
    from .src.hermes_research_report.academic import (
        ACADEMIC_PROTOCOL_ASSESS_SCHEMA,
        META_ANALYSIS_ASSESS_SCHEMA,
        assess_academic_protocol,
        assess_meta_analysis,
    )
    from .src.hermes_research_report.academic_integrity import (
        ACADEMIC_INTEGRITY_ASSESS_SCHEMA,
        assess_academic_integrity,
    )
    from .src.hermes_research_report.acquisition_integrity import (
        ACQUISITION_INTEGRITY_SCHEMA,
        assess_acquisition_integrity,
    )
    from .src.hermes_research_report.advanced_academic import (
        ACADEMIC_SYNTHESIS_GATE_SCHEMA,
        CERTAINTY_ASSESS_SCHEMA,
        COMPUTATION_REPLAY_ASSESS_SCHEMA,
        EXTRACTION_ASSESS_SCHEMA,
        FIXED_EFFECT_COMPUTE_SCHEMA,
        PRISMA_ASSESS_SCHEMA,
        PRISMA_FLOW_ACCOUNT_SCHEMA,
        REVIEW_PROTOCOL_VALIDATE_SCHEMA,
        RISK_OF_BIAS_ASSESS_SCHEMA,
        SCREENING_ADJUDICATE_SCHEMA,
        STUDY_GRAPH_RESOLVE_SCHEMA,
        adjudicate_screening,
        assess_academic_synthesis_gate,
        assess_certainty,
        assess_computation_replay,
        assess_extraction,
        assess_prisma,
        assess_prisma_flow_accounting,
        assess_risk_of_bias,
        compute_fixed_effect_estimate,
        resolve_study_graph,
        validate_review_protocol,
    )
    from .src.hermes_research_report.artifacts import assess_artifact
    from .src.hermes_research_report.attribution import (
        ATTRIBUTION_ASSESS_SCHEMA,
        NARRATIVE_DIFF_ASSESS_SCHEMA,
        SOURCE_INFLUENCE_ASSESS_SCHEMA,
        assess_attribution,
        assess_narrative_diff,
        assess_source_influence,
    )
    from .src.hermes_research_report.beta_modes import (
        BETA_MODE_PLAN_BUILD_SCHEMA,
        build_beta_mode_plan,
    )
    from .src.hermes_research_report.briefing import (
        BRIEF_BUILD_SCHEMA,
        CONTEXT_PACKAGE_BUILD_SCHEMA,
        CONTEXTUALIZATION_BUILD_SCHEMA,
        DEBRIEF_ASSESS_SCHEMA,
        assess_debrief,
        build_brief,
        build_context_package,
        build_contextualization,
    )
    from .src.hermes_research_report.budget import BUDGET_ASSESS_SCHEMA, assess_budget
    from .src.hermes_research_report.business import (
        BUSINESS_DESIGN_ASSESS_SCHEMA,
        assess_business_design,
    )
    from .src.hermes_research_report.business_controls import (
        BUSINESS_CONTROL_ASSESS_SCHEMA,
        assess_business_control,
    )
    from .src.hermes_research_report.circuit import assess_circuit
    from .src.hermes_research_report.claim_verification import (
        CLAIM_VERIFICATION_GRAPH_SCHEMA,
        assess_claim_verification_graph,
    )
    from .src.hermes_research_report.claims import (
        CHALLENGE_EVALUATE_SCHEMA,
        CLAIM_EVALUATE_SCHEMA,
        SYNTHESIS_ASSESS_SCHEMA,
        assess_synthesis,
        evaluate_challenge,
        evaluate_claim,
    )
    from .src.hermes_research_report.collaboration import (
        CONSILIUM_PLAN_ASSESS_SCHEMA,
        CONSILIUM_RESULT_ASSESS_SCHEMA,
        MODALITY_PLAN_ASSESS_SCHEMA,
        ROLE_INDEPENDENCE_ASSESS_SCHEMA,
        ROLE_PROFILE_ASSESS_SCHEMA,
        TOPOLOGY_SELECT_SCHEMA,
        assess_consilium_plan,
        assess_consilium_result,
        assess_modality_plan,
        assess_role_independence,
        assess_role_profile,
        select_topology,
    )
    from .src.hermes_research_report.comparison import (
        COMPARISON_TOOL_SCHEMA,
        compare_periods,
    )
    from .src.hermes_research_report.context_lifecycle import assess_context_lifecycle
    from .src.hermes_research_report.corpus import (
        CORPUS_MATERIALIZE_SCHEMA,
        materialize_corpus,
    )
    from .src.hermes_research_report.coverage_details import (
        SEARCH_COVERAGE_DETAILS_SCHEMA,
        assess_search_coverage_details,
    )
    from .src.hermes_research_report.coverage_status import (
        COVERAGE_STATUS_ASSESS_SCHEMA,
        assess_coverage_status,
    )
    from .src.hermes_research_report.decisions import (
        DECISION_ENVELOPE_ASSESS_SCHEMA,
        DELTA_ASSESS_SCHEMA,
        INCIDENT_ASSESS_SCHEMA,
        INDEPENDENT_SUPPORT_ASSESS_SCHEMA,
        assess_decision_envelope,
        assess_delta,
        assess_incident,
        assess_independent_support,
    )
    from .src.hermes_research_report.decomposition import (
        CONSTRUCT_OPERATIONALIZE_SCHEMA,
        CONSTRUCT_REVISE_SCHEMA,
        DECOMPOSITION_ASSESS_SCHEMA,
        assess_decomposition,
        operationalize_construct,
        propose_construct_revision,
    )
    from .src.hermes_research_report.deep_qualification import (
        DEEP_QUALIFICATION_ASSESS_SCHEMA,
        MULTIAGENT_INDEPENDENCE_ASSESS_SCHEMA,
        OBLIGATION_PRESERVATION_ASSESS_SCHEMA,
        RESILIENCE_RECOVERY_ASSESS_SCHEMA,
        assess_deep_qualification,
        assess_multiagent_independence,
        assess_obligation_preservation,
        assess_resilience_recovery,
    )
    from .src.hermes_research_report.deployment import (
        MIGRATION_MAP_SCHEMA,
        RESOURCE_ADMISSION_SCHEMA,
        assess_resource_admission,
        dry_run_migration_map,
    )
    from .src.hermes_research_report.document_graph import (
        DOCUMENT_GRAPH_BUILD_SCHEMA,
        DOCUMENT_GRAPH_VERIFY_SCHEMA,
        build_document_graph,
        verify_document_graph,
    )
    from .src.hermes_research_report.dolt import assess_dolt_commit
    from .src.hermes_research_report.engagement import (
        ENGAGEMENT_LEVEL_REVISE_SCHEMA,
        ENGAGEMENT_LEVEL_SELECT_SCHEMA,
        PARSING_RESULT_ASSESS_SCHEMA,
        assess_parsing_result,
        propose_engagement_level_revision,
        select_engagement_level,
    )
    from .src.hermes_research_report.epistemics import (
        CLAIM_CARD_ASSESS_SCHEMA,
        EVIDENCE_EXCEPTION_ASSESS_SCHEMA,
        EVIDENCE_STANDARD_CREATE_SCHEMA,
        EVIDENCE_STANDARD_REVISE_SCHEMA,
        NEGATIVE_KNOWLEDGE_CLASSIFY_SCHEMA,
        assess_claim_card,
        assess_evidence_exception,
        classify_negative_knowledge,
        create_evidence_standard,
        propose_evidence_standard_revision,
    )
    from .src.hermes_research_report.errors import ContractError
    from .src.hermes_research_report.evidence import promote_fragment
    from .src.hermes_research_report.foundation import assess_foundation
    from .src.hermes_research_report.governance import (
        ASSURANCE_PROFILE_ASSESS_SCHEMA,
        BASIC_LOOP_ASSESS_SCHEMA,
        OVERSIGHT_TRANSITIONS_ASSESS_SCHEMA,
        assess_assurance_profile,
        assess_basic_loop,
        assess_oversight_transitions,
    )
    from .src.hermes_research_report.greenfield import (
        accept_greenfield,
        assess_greenfield,
    )
    from .src.hermes_research_report.installation import assess_installation
    from .src.hermes_research_report.instruments import (
        INSTRUMENT_PORTFOLIO_BUILD_SCHEMA,
        INSTRUMENT_STRATEGY_BUILD_SCHEMA,
        INSTRUMENT_STRATEGY_REVISE_SCHEMA,
        TOOL_QUERY_BUILD_SCHEMA,
        build_instrument_portfolio,
        build_instrument_strategy,
        build_tool_query,
        propose_instrument_strategy_revision,
    )
    from .src.hermes_research_report.intake import (
        PARSE_INTAKE_ASSESS_SCHEMA,
        PARSE_RUNS_RECORD_SCHEMA,
        UNICODE_REPRESENTATIONS_BUILD_SCHEMA,
        assess_parse_intake,
        build_unicode_representations,
        record_parse_runs,
    )
    from .src.hermes_research_report.knowledge import (
        FACT_MAP_BUILD_SCHEMA,
        PROJECTIONS_RECONCILE_SCHEMA,
        ROOT_CAUSE_MAP_BUILD_SCHEMA,
        build_fact_map,
        build_root_cause_map,
        reconcile_knowledge_projections,
    )
    from .src.hermes_research_report.lifecycle import (
        CONTEXT_ASSEMBLY_ASSESS_SCHEMA,
        INVALIDATION_ASSESS_SCHEMA,
        OBJECT_REVISION_ASSESS_SCHEMA,
        RESTORE_ASSESS_SCHEMA,
        assess_context_assembly,
        assess_invalidation,
        assess_object_revision,
        assess_restore,
    )
    from .src.hermes_research_report.narrative import (
        NARRATIVE_PLAN_ASSESS_SCHEMA,
        assess_narrative_plan,
    )
    from .src.hermes_research_report.numeric_reproduction import (
        NUMERIC_REPRODUCTION_SCHEMA,
        assess_numeric_reproduction,
    )
    from .src.hermes_research_report.orchestration import (
        WORK_PLAN_BUILD_SCHEMA,
        build_work_plan,
    )
    from .src.hermes_research_report.portability import (
        BUNDLE_IMPORT_ASSESS_SCHEMA,
        LEGACY_MIGRATION_ASSESS_SCHEMA,
        OPERATION_RECONCILE_SCHEMA,
        RECOVERY_ASSESS_SCHEMA,
        assess_bundle_import,
        assess_legacy_migration,
        assess_recovery,
        reconcile_operation,
    )
    from .src.hermes_research_report.provenance import (
        LIVING_REVIEW_ASSESS_SCHEMA,
        PROVENANCE_EXPORT_ASSESS_SCHEMA,
        REPLAY_ASSESS_SCHEMA,
        assess_living_review,
        assess_provenance_export,
        assess_replay,
    )
    from .src.hermes_research_report.provider_contracts import (
        PROVIDER_BUDGET_RESERVE_SCHEMA,
        PROVIDER_CATALOG_GET_SCHEMA,
        PROVIDER_CONFORMANCE_ASSESS_SCHEMA,
        PROVIDER_FALLBACK_ASSESS_SCHEMA,
        PROVIDER_LIFECYCLE_RECONCILE_SCHEMA,
        PROVIDER_MANIFEST_BUILD_SCHEMA,
        PROVIDER_OPERATION_ASSESS_SCHEMA,
        PROVIDER_RECEIPT_NORMALIZE_SCHEMA,
        PROVIDER_SCHEMA_DIFF_SCHEMA,
        assess_provider_conformance,
        assess_provider_fallback,
        assess_provider_operation,
        build_provider_manifest,
        diff_provider_schema,
        get_provider_catalog,
        normalize_provider_receipt,
        reconcile_provider_lifecycle,
        reserve_provider_budget,
    )
    from .src.hermes_research_report.provider_execution import (
        PROVIDER_EXECUTION_ASSESS_SCHEMA,
        assess_provider_execution,
    )
    from .src.hermes_research_report.provider_live import (
        PROVIDER_LIVE_PROBE_SCHEMA,
        probe_provider_live,
    )
    from .src.hermes_research_report.qualification import (
        DEPLOYMENT_CANDIDATE_SCHEMA,
        DEPTH_COMPARISON_SCHEMA,
        PROFILE_QUALIFICATION_SCHEMA,
        UTILITY_ASSESS_SCHEMA,
        assess_deployment_candidate,
        assess_utility,
        compare_depths,
        evaluate_profile_qualification,
    )
    from .src.hermes_research_report.r3_evidence import (
        R3_EVIDENCE_SCHEMA,
        assess_r3_evidence_field,
    )
    from .src.hermes_research_report.report import (
        REPORT_TOOL_SCHEMA,
        ReportInputError,
        build_report,
    )
    from .src.hermes_research_report.review_release import (
        ACCEPTANCE_ASSESS_SCHEMA,
        CORRECTION_ASSESS_SCHEMA,
        RELEASE_ASSESS_SCHEMA,
        REVIEW_ASSESS_SCHEMA,
        assess_acceptance,
        assess_correction,
        assess_release,
        assess_review,
    )
    from .src.hermes_research_report.routing import ROUTE_ASSESS_SCHEMA, assess_route
    from .src.hermes_research_report.run_contract import (
        RUN_CONTRACT_CREATE_SCHEMA,
        RUN_CONTRACT_REVISE_SCHEMA,
        create_run_contract,
        propose_run_contract_revision,
    )
    from .src.hermes_research_report.runtime_contracts import (
        CAPABILITY_MODEL_SCHEMA,
        CONTEXT_ASSEMBLY_SCHEMA,
        DISTRIBUTION_DELIVERY_SCHEMA,
        LIVENESS_RECONCILE_SCHEMA,
        assemble_context_package,
        assess_capability_model_lane,
        assess_distribution_delivery,
        reconcile_work_liveness,
    )
    from .src.hermes_research_report.schemas import (
        ARTIFACT_ASSESS_SCHEMA,
        CIRCUIT_ASSESS_SCHEMA,
        CONTEXT_LIFECYCLE_SCHEMA,
        DOLT_COMMIT_ASSESS_SCHEMA,
        FOUNDATION_ASSESS_SCHEMA,
        FRAGMENT_PROMOTE_SCHEMA,
        GREENFIELD_ACCEPT_SCHEMA,
        GREENFIELD_ASSESS_SCHEMA,
        INSTALLATION_ASSESS_SCHEMA,
        STATE_RECONCILE_SCHEMA,
    )
    from .src.hermes_research_report.scholarly import (
        CAPABILITY_GAP_ASSESS_SCHEMA,
        SCHOLARLY_OBJECT_RESOLVE_SCHEMA,
        assess_capability_gap,
        resolve_scholarly_object,
    )
    from .src.hermes_research_report.search_execution import (
        SEARCH_EXECUTION_TRACE_SCHEMA,
        assess_search_execution_trace,
    )
    from .src.hermes_research_report.search_ledger import (
        SEARCH_LEDGER_ASSESS_SCHEMA,
        assess_search_ledger,
    )
    from .src.hermes_research_report.search_workflow import (
        QUERY_AST_COMPILE_SCHEMA,
        SCREENING_STOP_ASSESS_SCHEMA,
        SEARCH_ENVIRONMENT_RECORD_SCHEMA,
        SEARCH_STOP_ASSESS_SCHEMA,
        SEARCH_STRATEGY_ASSESS_SCHEMA,
        assess_screening_stop,
        assess_search_stop,
        assess_search_strategy,
        compile_query_ast,
        record_search_environment,
    )
    from .src.hermes_research_report.security_controls import (
        SECURITY_CONTROL_ASSESS_SCHEMA,
        assess_security_control,
    )
    from .src.hermes_research_report.source_families import (
        SEARCH_COVERAGE_ASSESS_SCHEMA,
        SOURCE_POOL_AUDIT_SCHEMA,
        assess_search_coverage,
        audit_source_pool,
    )
    from .src.hermes_research_report.sources import (
        FRAGMENT_VERIFY_SCHEMA,
        SOURCE_SELECT_SCHEMA,
        select_source,
        verify_fragment,
    )
    from .src.hermes_research_report.state import reconcile_state
    from .src.hermes_research_report.state_semantics import (
        STATE_SEMANTICS_ASSESS_SCHEMA,
        assess_state_semantics,
    )
    from .src.hermes_research_report.udr import (
        QUALITY_DASHBOARD_PROJECT_SCHEMA,
        UDR_ARCHITECTURE_SELECT_SCHEMA,
        UDR_PLAN_ASSESS_SCHEMA,
        assess_udr_plan,
        project_quality_dashboard,
        select_udr_architecture,
    )
    from .src.hermes_research_report.work_execution import (
        WORK_EXECUTION_ASSESS_SCHEMA,
        assess_work_execution,
    )
except ImportError:  # Installed wheel/module execution.
    from hermes_research_report.academic import (
        ACADEMIC_PROTOCOL_ASSESS_SCHEMA,
        META_ANALYSIS_ASSESS_SCHEMA,
        assess_academic_protocol,
        assess_meta_analysis,
    )
    from hermes_research_report.academic_integrity import (
        ACADEMIC_INTEGRITY_ASSESS_SCHEMA,
        assess_academic_integrity,
    )
    from hermes_research_report.acquisition_integrity import (
        ACQUISITION_INTEGRITY_SCHEMA,
        assess_acquisition_integrity,
    )
    from hermes_research_report.advanced_academic import (
        ACADEMIC_SYNTHESIS_GATE_SCHEMA,
        CERTAINTY_ASSESS_SCHEMA,
        COMPUTATION_REPLAY_ASSESS_SCHEMA,
        EXTRACTION_ASSESS_SCHEMA,
        FIXED_EFFECT_COMPUTE_SCHEMA,
        PRISMA_ASSESS_SCHEMA,
        PRISMA_FLOW_ACCOUNT_SCHEMA,
        REVIEW_PROTOCOL_VALIDATE_SCHEMA,
        RISK_OF_BIAS_ASSESS_SCHEMA,
        SCREENING_ADJUDICATE_SCHEMA,
        STUDY_GRAPH_RESOLVE_SCHEMA,
        adjudicate_screening,
        assess_academic_synthesis_gate,
        assess_certainty,
        assess_computation_replay,
        assess_extraction,
        assess_prisma,
        assess_prisma_flow_accounting,
        assess_risk_of_bias,
        compute_fixed_effect_estimate,
        resolve_study_graph,
        validate_review_protocol,
    )
    from hermes_research_report.artifacts import assess_artifact
    from hermes_research_report.attribution import (
        ATTRIBUTION_ASSESS_SCHEMA,
        NARRATIVE_DIFF_ASSESS_SCHEMA,
        SOURCE_INFLUENCE_ASSESS_SCHEMA,
        assess_attribution,
        assess_narrative_diff,
        assess_source_influence,
    )
    from hermes_research_report.beta_modes import (
        BETA_MODE_PLAN_BUILD_SCHEMA,
        build_beta_mode_plan,
    )
    from hermes_research_report.briefing import (
        BRIEF_BUILD_SCHEMA,
        CONTEXT_PACKAGE_BUILD_SCHEMA,
        CONTEXTUALIZATION_BUILD_SCHEMA,
        DEBRIEF_ASSESS_SCHEMA,
        assess_debrief,
        build_brief,
        build_context_package,
        build_contextualization,
    )
    from hermes_research_report.budget import BUDGET_ASSESS_SCHEMA, assess_budget
    from hermes_research_report.business import (
        BUSINESS_DESIGN_ASSESS_SCHEMA,
        assess_business_design,
    )
    from hermes_research_report.business_controls import (
        BUSINESS_CONTROL_ASSESS_SCHEMA,
        assess_business_control,
    )
    from hermes_research_report.circuit import assess_circuit
    from hermes_research_report.claim_verification import (
        CLAIM_VERIFICATION_GRAPH_SCHEMA,
        assess_claim_verification_graph,
    )
    from hermes_research_report.claims import (
        CHALLENGE_EVALUATE_SCHEMA,
        CLAIM_EVALUATE_SCHEMA,
        SYNTHESIS_ASSESS_SCHEMA,
        assess_synthesis,
        evaluate_challenge,
        evaluate_claim,
    )
    from hermes_research_report.collaboration import (
        CONSILIUM_PLAN_ASSESS_SCHEMA,
        CONSILIUM_RESULT_ASSESS_SCHEMA,
        MODALITY_PLAN_ASSESS_SCHEMA,
        ROLE_INDEPENDENCE_ASSESS_SCHEMA,
        ROLE_PROFILE_ASSESS_SCHEMA,
        TOPOLOGY_SELECT_SCHEMA,
        assess_consilium_plan,
        assess_consilium_result,
        assess_modality_plan,
        assess_role_independence,
        assess_role_profile,
        select_topology,
    )
    from hermes_research_report.comparison import (
        COMPARISON_TOOL_SCHEMA,
        compare_periods,
    )
    from hermes_research_report.context_lifecycle import assess_context_lifecycle
    from hermes_research_report.corpus import (
        CORPUS_MATERIALIZE_SCHEMA,
        materialize_corpus,
    )
    from hermes_research_report.coverage_details import (
        SEARCH_COVERAGE_DETAILS_SCHEMA,
        assess_search_coverage_details,
    )
    from hermes_research_report.coverage_status import (
        COVERAGE_STATUS_ASSESS_SCHEMA,
        assess_coverage_status,
    )
    from hermes_research_report.decisions import (
        DECISION_ENVELOPE_ASSESS_SCHEMA,
        DELTA_ASSESS_SCHEMA,
        INCIDENT_ASSESS_SCHEMA,
        INDEPENDENT_SUPPORT_ASSESS_SCHEMA,
        assess_decision_envelope,
        assess_delta,
        assess_incident,
        assess_independent_support,
    )
    from hermes_research_report.decomposition import (
        CONSTRUCT_OPERATIONALIZE_SCHEMA,
        CONSTRUCT_REVISE_SCHEMA,
        DECOMPOSITION_ASSESS_SCHEMA,
        assess_decomposition,
        operationalize_construct,
        propose_construct_revision,
    )
    from hermes_research_report.deep_qualification import (
        DEEP_QUALIFICATION_ASSESS_SCHEMA,
        MULTIAGENT_INDEPENDENCE_ASSESS_SCHEMA,
        OBLIGATION_PRESERVATION_ASSESS_SCHEMA,
        RESILIENCE_RECOVERY_ASSESS_SCHEMA,
        assess_deep_qualification,
        assess_multiagent_independence,
        assess_obligation_preservation,
        assess_resilience_recovery,
    )
    from hermes_research_report.deployment import (
        MIGRATION_MAP_SCHEMA,
        RESOURCE_ADMISSION_SCHEMA,
        assess_resource_admission,
        dry_run_migration_map,
    )
    from hermes_research_report.document_graph import (
        DOCUMENT_GRAPH_BUILD_SCHEMA,
        DOCUMENT_GRAPH_VERIFY_SCHEMA,
        build_document_graph,
        verify_document_graph,
    )
    from hermes_research_report.dolt import assess_dolt_commit
    from hermes_research_report.engagement import (
        ENGAGEMENT_LEVEL_REVISE_SCHEMA,
        ENGAGEMENT_LEVEL_SELECT_SCHEMA,
        PARSING_RESULT_ASSESS_SCHEMA,
        assess_parsing_result,
        propose_engagement_level_revision,
        select_engagement_level,
    )
    from hermes_research_report.epistemics import (
        CLAIM_CARD_ASSESS_SCHEMA,
        EVIDENCE_EXCEPTION_ASSESS_SCHEMA,
        EVIDENCE_STANDARD_CREATE_SCHEMA,
        EVIDENCE_STANDARD_REVISE_SCHEMA,
        NEGATIVE_KNOWLEDGE_CLASSIFY_SCHEMA,
        assess_claim_card,
        assess_evidence_exception,
        classify_negative_knowledge,
        create_evidence_standard,
        propose_evidence_standard_revision,
    )
    from hermes_research_report.errors import ContractError
    from hermes_research_report.evidence import promote_fragment
    from hermes_research_report.foundation import assess_foundation
    from hermes_research_report.governance import (
        ASSURANCE_PROFILE_ASSESS_SCHEMA,
        BASIC_LOOP_ASSESS_SCHEMA,
        OVERSIGHT_TRANSITIONS_ASSESS_SCHEMA,
        assess_assurance_profile,
        assess_basic_loop,
        assess_oversight_transitions,
    )
    from hermes_research_report.greenfield import accept_greenfield, assess_greenfield
    from hermes_research_report.installation import assess_installation
    from hermes_research_report.instruments import (
        INSTRUMENT_PORTFOLIO_BUILD_SCHEMA,
        INSTRUMENT_STRATEGY_BUILD_SCHEMA,
        INSTRUMENT_STRATEGY_REVISE_SCHEMA,
        TOOL_QUERY_BUILD_SCHEMA,
        build_instrument_portfolio,
        build_instrument_strategy,
        build_tool_query,
        propose_instrument_strategy_revision,
    )
    from hermes_research_report.intake import (
        PARSE_INTAKE_ASSESS_SCHEMA,
        PARSE_RUNS_RECORD_SCHEMA,
        UNICODE_REPRESENTATIONS_BUILD_SCHEMA,
        assess_parse_intake,
        build_unicode_representations,
        record_parse_runs,
    )
    from hermes_research_report.knowledge import (
        FACT_MAP_BUILD_SCHEMA,
        PROJECTIONS_RECONCILE_SCHEMA,
        ROOT_CAUSE_MAP_BUILD_SCHEMA,
        build_fact_map,
        build_root_cause_map,
        reconcile_knowledge_projections,
    )
    from hermes_research_report.lifecycle import (
        CONTEXT_ASSEMBLY_ASSESS_SCHEMA,
        INVALIDATION_ASSESS_SCHEMA,
        OBJECT_REVISION_ASSESS_SCHEMA,
        RESTORE_ASSESS_SCHEMA,
        assess_context_assembly,
        assess_invalidation,
        assess_object_revision,
        assess_restore,
    )
    from hermes_research_report.narrative import (
        NARRATIVE_PLAN_ASSESS_SCHEMA,
        assess_narrative_plan,
    )
    from hermes_research_report.numeric_reproduction import (
        NUMERIC_REPRODUCTION_SCHEMA,
        assess_numeric_reproduction,
    )
    from hermes_research_report.orchestration import (
        WORK_PLAN_BUILD_SCHEMA,
        build_work_plan,
    )
    from hermes_research_report.portability import (
        BUNDLE_IMPORT_ASSESS_SCHEMA,
        LEGACY_MIGRATION_ASSESS_SCHEMA,
        OPERATION_RECONCILE_SCHEMA,
        RECOVERY_ASSESS_SCHEMA,
        assess_bundle_import,
        assess_legacy_migration,
        assess_recovery,
        reconcile_operation,
    )
    from hermes_research_report.provenance import (
        LIVING_REVIEW_ASSESS_SCHEMA,
        PROVENANCE_EXPORT_ASSESS_SCHEMA,
        REPLAY_ASSESS_SCHEMA,
        assess_living_review,
        assess_provenance_export,
        assess_replay,
    )
    from hermes_research_report.provider_contracts import (
        PROVIDER_BUDGET_RESERVE_SCHEMA,
        PROVIDER_CATALOG_GET_SCHEMA,
        PROVIDER_CONFORMANCE_ASSESS_SCHEMA,
        PROVIDER_FALLBACK_ASSESS_SCHEMA,
        PROVIDER_LIFECYCLE_RECONCILE_SCHEMA,
        PROVIDER_MANIFEST_BUILD_SCHEMA,
        PROVIDER_OPERATION_ASSESS_SCHEMA,
        PROVIDER_RECEIPT_NORMALIZE_SCHEMA,
        PROVIDER_SCHEMA_DIFF_SCHEMA,
        assess_provider_conformance,
        assess_provider_fallback,
        assess_provider_operation,
        build_provider_manifest,
        diff_provider_schema,
        get_provider_catalog,
        normalize_provider_receipt,
        reconcile_provider_lifecycle,
        reserve_provider_budget,
    )
    from hermes_research_report.provider_execution import (
        PROVIDER_EXECUTION_ASSESS_SCHEMA,
        assess_provider_execution,
    )
    from hermes_research_report.provider_live import (
        PROVIDER_LIVE_PROBE_SCHEMA,
        probe_provider_live,
    )
    from hermes_research_report.qualification import (
        DEPLOYMENT_CANDIDATE_SCHEMA,
        DEPTH_COMPARISON_SCHEMA,
        PROFILE_QUALIFICATION_SCHEMA,
        UTILITY_ASSESS_SCHEMA,
        assess_deployment_candidate,
        assess_utility,
        compare_depths,
        evaluate_profile_qualification,
    )
    from hermes_research_report.r3_evidence import (
        R3_EVIDENCE_SCHEMA,
        assess_r3_evidence_field,
    )
    from hermes_research_report.report import (
        REPORT_TOOL_SCHEMA,
        ReportInputError,
        build_report,
    )
    from hermes_research_report.review_release import (
        ACCEPTANCE_ASSESS_SCHEMA,
        CORRECTION_ASSESS_SCHEMA,
        RELEASE_ASSESS_SCHEMA,
        REVIEW_ASSESS_SCHEMA,
        assess_acceptance,
        assess_correction,
        assess_release,
        assess_review,
    )
    from hermes_research_report.routing import ROUTE_ASSESS_SCHEMA, assess_route
    from hermes_research_report.run_contract import (
        RUN_CONTRACT_CREATE_SCHEMA,
        RUN_CONTRACT_REVISE_SCHEMA,
        create_run_contract,
        propose_run_contract_revision,
    )
    from hermes_research_report.runtime_contracts import (
        CAPABILITY_MODEL_SCHEMA,
        CONTEXT_ASSEMBLY_SCHEMA,
        DISTRIBUTION_DELIVERY_SCHEMA,
        LIVENESS_RECONCILE_SCHEMA,
        assemble_context_package,
        assess_capability_model_lane,
        assess_distribution_delivery,
        reconcile_work_liveness,
    )
    from hermes_research_report.schemas import (
        ARTIFACT_ASSESS_SCHEMA,
        CIRCUIT_ASSESS_SCHEMA,
        CONTEXT_LIFECYCLE_SCHEMA,
        DOLT_COMMIT_ASSESS_SCHEMA,
        FOUNDATION_ASSESS_SCHEMA,
        FRAGMENT_PROMOTE_SCHEMA,
        GREENFIELD_ACCEPT_SCHEMA,
        GREENFIELD_ASSESS_SCHEMA,
        INSTALLATION_ASSESS_SCHEMA,
        STATE_RECONCILE_SCHEMA,
    )
    from hermes_research_report.scholarly import (
        CAPABILITY_GAP_ASSESS_SCHEMA,
        SCHOLARLY_OBJECT_RESOLVE_SCHEMA,
        assess_capability_gap,
        resolve_scholarly_object,
    )
    from hermes_research_report.search_execution import (
        SEARCH_EXECUTION_TRACE_SCHEMA,
        assess_search_execution_trace,
    )
    from hermes_research_report.search_ledger import (
        SEARCH_LEDGER_ASSESS_SCHEMA,
        assess_search_ledger,
    )
    from hermes_research_report.search_workflow import (
        QUERY_AST_COMPILE_SCHEMA,
        SCREENING_STOP_ASSESS_SCHEMA,
        SEARCH_ENVIRONMENT_RECORD_SCHEMA,
        SEARCH_STOP_ASSESS_SCHEMA,
        SEARCH_STRATEGY_ASSESS_SCHEMA,
        assess_screening_stop,
        assess_search_stop,
        assess_search_strategy,
        compile_query_ast,
        record_search_environment,
    )
    from hermes_research_report.security_controls import (
        SECURITY_CONTROL_ASSESS_SCHEMA,
        assess_security_control,
    )
    from hermes_research_report.source_families import (
        SEARCH_COVERAGE_ASSESS_SCHEMA,
        SOURCE_POOL_AUDIT_SCHEMA,
        assess_search_coverage,
        audit_source_pool,
    )
    from hermes_research_report.sources import (
        FRAGMENT_VERIFY_SCHEMA,
        SOURCE_SELECT_SCHEMA,
        select_source,
        verify_fragment,
    )
    from hermes_research_report.state import reconcile_state
    from hermes_research_report.state_semantics import (
        STATE_SEMANTICS_ASSESS_SCHEMA,
        assess_state_semantics,
    )
    from hermes_research_report.udr import (
        QUALITY_DASHBOARD_PROJECT_SCHEMA,
        UDR_ARCHITECTURE_SELECT_SCHEMA,
        UDR_PLAN_ASSESS_SCHEMA,
        assess_udr_plan,
        project_quality_dashboard,
        select_udr_architecture,
    )
    from hermes_research_report.work_execution import (
        WORK_EXECUTION_ASSESS_SCHEMA,
        assess_work_execution,
    )


def _handle(function: Callable[[object], dict[str, Any]], args: object) -> str:
    try:
        result = function(args)
    except ContractError as error:
        result = {"status": "error", "error": error.as_dict()}
    except (TypeError, ValueError) as error:
        result = {
            "status": "error",
            "error": {
                "code": "invalid_request",
                "path": "request",
                "message": type(error).__name__,
            },
        }
    return json.dumps(
        result,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def handle_greenfield_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_greenfield, args)


def handle_comparison(args: object, **_kwargs: object) -> str:
    try:
        if type(args) is not dict or set(args) != {
            "observations",
            "before",
            "after",
        }:
            raise ValueError(
                "Нужны observations, before и after без дополнительных полей."
            )
        result = compare_periods(args["observations"], args["before"], args["after"])
    except ValueError as error:
        result = {
            "status": "error",
            "error": {"code": "invalid_comparison", "message": str(error)},
        }
    return json.dumps(result, ensure_ascii=False, allow_nan=False)


def handle_report(args: object, **_kwargs: object) -> str:
    try:
        result = build_report(args)
    except ReportInputError as error:
        result = {
            "status": "error",
            "error": {
                "code": error.code,
                "path": error.path,
                "message": str(error),
            },
        }
    return json.dumps(result, ensure_ascii=False, allow_nan=False)


def handle_contract_create(args: object, **_kwargs: object) -> str:
    return _handle(create_run_contract, args)


def handle_contract_revision(args: object, **_kwargs: object) -> str:
    return _handle(propose_run_contract_revision, args)


def handle_budget_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_budget, args)


def handle_beta_mode_plan_build(args: object, **_kwargs: object) -> str:
    return _handle(build_beta_mode_plan, args)


def handle_plan_build(args: object, **_kwargs: object) -> str:
    return _handle(build_work_plan, args)


def handle_work_execution_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_work_execution, args)


def handle_route_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_route, args)


def handle_search_ledger_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_ledger, args)


def handle_search_execution_trace_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_execution_trace, args)


def handle_search_coverage_details_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_coverage_details, args)


def handle_coverage_status_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_coverage_status, args)


def handle_corpus_materialize(args: object, **_kwargs: object) -> str:
    return _handle(materialize_corpus, args)


def handle_acquisition_integrity_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_acquisition_integrity, args)


def handle_source_select(args: object, **_kwargs: object) -> str:
    return _handle(select_source, args)


def handle_fragment_verify(args: object, **_kwargs: object) -> str:
    return _handle(verify_fragment, args)


def handle_claim_evaluate(args: object, **_kwargs: object) -> str:
    return _handle(evaluate_claim, args)


def handle_claim_verification_graph_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_claim_verification_graph, args)


def handle_numeric_reproduction_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_numeric_reproduction, args)


def handle_challenge_evaluate(args: object, **_kwargs: object) -> str:
    return _handle(evaluate_challenge, args)


def handle_synthesis_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_synthesis, args)


def handle_evidence_standard_create(args: object, **_kwargs: object) -> str:
    return _handle(create_evidence_standard, args)


def handle_evidence_standard_revision(args: object, **_kwargs: object) -> str:
    return _handle(propose_evidence_standard_revision, args)


def handle_evidence_exception_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_evidence_exception, args)


def handle_claim_card_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_claim_card, args)


def handle_negative_knowledge_classify(args: object, **_kwargs: object) -> str:
    return _handle(classify_negative_knowledge, args)


def handle_search_coverage_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_coverage, args)


def handle_source_pool_audit(args: object, **_kwargs: object) -> str:
    return _handle(audit_source_pool, args)


def handle_udr_architecture_select(args: object, **_kwargs: object) -> str:
    return _handle(select_udr_architecture, args)


def handle_udr_plan_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_udr_plan, args)


def handle_quality_dashboard_project(args: object, **_kwargs: object) -> str:
    return _handle(project_quality_dashboard, args)


def handle_decision_envelope_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_decision_envelope, args)


def handle_delta_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_delta, args)


def handle_incident_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_incident, args)


def handle_independent_support_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_independent_support, args)


def handle_engagement_level_select(args: object, **_kwargs: object) -> str:
    return _handle(select_engagement_level, args)


def handle_engagement_level_revision(args: object, **_kwargs: object) -> str:
    return _handle(propose_engagement_level_revision, args)


def handle_parsing_result_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_parsing_result, args)


def handle_parse_intake_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_parse_intake, args)


def handle_parse_runs_record(args: object, **_kwargs: object) -> str:
    return _handle(record_parse_runs, args)


def handle_unicode_representations_build(args: object, **_kwargs: object) -> str:
    return _handle(build_unicode_representations, args)


def handle_document_graph_build(args: object, **_kwargs: object) -> str:
    return _handle(build_document_graph, args)


def handle_document_graph_verify(args: object, **_kwargs: object) -> str:
    return _handle(verify_document_graph, args)


def handle_query_ast_compile(args: object, **_kwargs: object) -> str:
    return _handle(compile_query_ast, args)


def handle_search_strategy_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_strategy, args)


def handle_search_environment_record(args: object, **_kwargs: object) -> str:
    return _handle(record_search_environment, args)


def handle_search_stop_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_search_stop, args)


def handle_screening_stop_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_screening_stop, args)


def handle_instrument_portfolio_build(args: object, **_kwargs: object) -> str:
    return _handle(build_instrument_portfolio, args)


def handle_instrument_strategy_build(args: object, **_kwargs: object) -> str:
    return _handle(build_instrument_strategy, args)


def handle_tool_query_build(args: object, **_kwargs: object) -> str:
    return _handle(build_tool_query, args)


def handle_instrument_strategy_revision(args: object, **_kwargs: object) -> str:
    return _handle(propose_instrument_strategy_revision, args)


def handle_brief_build(args: object, **_kwargs: object) -> str:
    return _handle(build_brief, args)


def handle_contextualization_build(args: object, **_kwargs: object) -> str:
    return _handle(build_contextualization, args)


def handle_context_package_build(args: object, **_kwargs: object) -> str:
    return _handle(build_context_package, args)


def handle_debrief_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_debrief, args)


def handle_decomposition_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_decomposition, args)


def handle_construct_operationalize(args: object, **_kwargs: object) -> str:
    return _handle(operationalize_construct, args)


def handle_construct_revision(args: object, **_kwargs: object) -> str:
    return _handle(propose_construct_revision, args)


def handle_assurance_profile_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_assurance_profile, args)


def handle_basic_loop_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_basic_loop, args)


def handle_oversight_transitions_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_oversight_transitions, args)


def handle_role_profile_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_role_profile, args)


def handle_role_independence_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_role_independence, args)


def handle_consilium_plan_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_consilium_plan, args)


def handle_consilium_result_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_consilium_result, args)


def handle_topology_select(args: object, **_kwargs: object) -> str:
    return _handle(select_topology, args)


def handle_modality_plan_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_modality_plan, args)


def handle_fact_map_build(args: object, **_kwargs: object) -> str:
    return _handle(build_fact_map, args)


def handle_root_cause_map_build(args: object, **_kwargs: object) -> str:
    return _handle(build_root_cause_map, args)


def handle_knowledge_projections_reconcile(args: object, **_kwargs: object) -> str:
    return _handle(reconcile_knowledge_projections, args)


def handle_narrative_plan_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_narrative_plan, args)


def handle_attribution_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_attribution, args)


def handle_source_influence_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_source_influence, args)


def handle_narrative_diff_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_narrative_diff, args)


def handle_provenance_export_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_provenance_export, args)


def handle_replay_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_replay, args)


def handle_living_review_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_living_review, args)


def handle_deep_qualification_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_deep_qualification, args)


def handle_obligation_preservation_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_obligation_preservation, args)


def handle_multiagent_independence_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_multiagent_independence, args)


def handle_resilience_recovery_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_resilience_recovery, args)


def handle_provider_catalog_get(args: object, **_kwargs: object) -> str:
    return _handle(get_provider_catalog, args)


def handle_provider_manifest_build(args: object, **_kwargs: object) -> str:
    return _handle(build_provider_manifest, args)


def handle_provider_schema_diff(args: object, **_kwargs: object) -> str:
    return _handle(diff_provider_schema, args)


def handle_provider_operation_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_provider_operation, args)


def handle_provider_execution_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_provider_execution, args)


def handle_provider_fallback_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_provider_fallback, args)


def handle_provider_budget_reserve(args: object, **_kwargs: object) -> str:
    return _handle(reserve_provider_budget, args)


def handle_provider_lifecycle_reconcile(args: object, **_kwargs: object) -> str:
    return _handle(reconcile_provider_lifecycle, args)


def handle_provider_receipt_normalize(args: object, **_kwargs: object) -> str:
    return _handle(normalize_provider_receipt, args)


def handle_provider_conformance_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_provider_conformance, args)


def handle_scholarly_object_resolve(args: object, **_kwargs: object) -> str:
    return _handle(resolve_scholarly_object, args)


def handle_capability_gap_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_capability_gap, args)


def handle_business_design_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_business_design, args)


def handle_business_control_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_business_control, args)


def handle_academic_protocol_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_academic_protocol, args)


def handle_academic_integrity_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_academic_integrity, args)


def handle_meta_analysis_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_meta_analysis, args)


def handle_review_protocol_validate(args: object, **_kwargs: object) -> str:
    return _handle(validate_review_protocol, args)


def handle_screening_adjudicate(args: object, **_kwargs: object) -> str:
    return _handle(adjudicate_screening, args)


def handle_study_graph_resolve(args: object, **_kwargs: object) -> str:
    return _handle(resolve_study_graph, args)


def handle_extraction_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_extraction, args)


def handle_prisma_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_prisma, args)


def handle_prisma_flow_account(args: object, **_kwargs: object) -> str:
    return _handle(assess_prisma_flow_accounting, args)


def handle_risk_of_bias_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_risk_of_bias, args)


def handle_certainty_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_certainty, args)


def handle_academic_synthesis_gate(args: object, **_kwargs: object) -> str:
    return _handle(assess_academic_synthesis_gate, args)


def handle_computation_replay_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_computation_replay, args)


def handle_fixed_effect_compute(args: object, **_kwargs: object) -> str:
    return _handle(compute_fixed_effect_estimate, args)


def handle_review_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_review, args)


def handle_acceptance_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_acceptance, args)


def handle_release_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_release, args)


def handle_correction_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_correction, args)


def handle_operation_reconcile(args: object, **_kwargs: object) -> str:
    return _handle(reconcile_operation, args)


def handle_recovery_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_recovery, args)


def handle_invalidation_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_invalidation, args)


def handle_object_revision_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_object_revision, args)


def handle_context_assembly_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_context_assembly, args)


def handle_restore_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_restore, args)


def handle_bundle_import_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_bundle_import, args)


def handle_legacy_migration_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_legacy_migration, args)


def handle_deployment_candidate_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_deployment_candidate, args)


def handle_profile_qualification(args: object, **_kwargs: object) -> str:
    return _handle(evaluate_profile_qualification, args)


def handle_depth_compare(args: object, **_kwargs: object) -> str:
    return _handle(compare_depths, args)


def handle_utility_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_utility, args)


def handle_greenfield_accept(args: object, **_kwargs: object) -> str:
    return _handle(accept_greenfield, args)


def handle_foundation_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_foundation, args)


def handle_resource_admission_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_resource_admission, args)


def handle_migration_map_dry_run(args: object, **_kwargs: object) -> str:
    return _handle(dry_run_migration_map, args)


def handle_state_reconcile(args: object, **_kwargs: object) -> str:
    return _handle(reconcile_state, args)


def handle_state_semantics_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_state_semantics, args)


def handle_security_control_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_security_control, args)


def handle_artifact_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_artifact, args)


def handle_fragment_promote(args: object, **_kwargs: object) -> str:
    return _handle(promote_fragment, args)


def handle_installation_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_installation, args)


def handle_context_lifecycle_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_context_lifecycle, args)


def handle_circuit_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_circuit, args)


def handle_capability_model_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_capability_model_lane, args)


def handle_provider_live_probe(args: object, **_kwargs: object) -> str:
    return _handle(probe_provider_live, args)


def handle_r3_evidence_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_r3_evidence_field, args)


def handle_context_package_assemble(args: object, **_kwargs: object) -> str:
    return _handle(assemble_context_package, args)


def handle_work_liveness_reconcile(args: object, **_kwargs: object) -> str:
    return _handle(reconcile_work_liveness, args)


def handle_distribution_delivery_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_distribution_delivery, args)


def handle_dolt_commit_assess(args: object, **_kwargs: object) -> str:
    return _handle(assess_dolt_commit, args)


def register(ctx: Any) -> None:
    ctx.register_tool(
        name="research_compare_periods",
        toolset="research",
        schema=COMPARISON_TOOL_SCHEMA,
        handler=handle_comparison,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_build_report",
        toolset="research",
        schema=REPORT_TOOL_SCHEMA,
        handler=handle_report,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_contract_create",
        toolset="research",
        schema=RUN_CONTRACT_CREATE_SCHEMA,
        handler=handle_contract_create,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_contract_propose_revision",
        toolset="research",
        schema=RUN_CONTRACT_REVISE_SCHEMA,
        handler=handle_contract_revision,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_budget_assess",
        toolset="research",
        schema=BUDGET_ASSESS_SCHEMA,
        handler=handle_budget_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_beta_mode_plan_build",
        toolset="research",
        schema=BETA_MODE_PLAN_BUILD_SCHEMA,
        handler=handle_beta_mode_plan_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_plan_build",
        toolset="research",
        schema=WORK_PLAN_BUILD_SCHEMA,
        handler=handle_plan_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_work_execution_assess",
        toolset="research",
        schema=WORK_EXECUTION_ASSESS_SCHEMA,
        handler=handle_work_execution_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_route_assess",
        toolset="research",
        schema=ROUTE_ASSESS_SCHEMA,
        handler=handle_route_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_ledger_assess",
        toolset="research",
        schema=SEARCH_LEDGER_ASSESS_SCHEMA,
        handler=handle_search_ledger_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_execution_trace_assess",
        toolset="research",
        schema=SEARCH_EXECUTION_TRACE_SCHEMA,
        handler=handle_search_execution_trace_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_coverage_details_assess",
        toolset="research",
        schema=SEARCH_COVERAGE_DETAILS_SCHEMA,
        handler=handle_search_coverage_details_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_coverage_status_assess",
        toolset="research",
        schema=COVERAGE_STATUS_ASSESS_SCHEMA,
        handler=handle_coverage_status_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_corpus_materialize",
        toolset="research",
        schema=CORPUS_MATERIALIZE_SCHEMA,
        handler=handle_corpus_materialize,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_acquisition_integrity_assess",
        toolset="research",
        schema=ACQUISITION_INTEGRITY_SCHEMA,
        handler=handle_acquisition_integrity_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_source_select",
        toolset="research",
        schema=SOURCE_SELECT_SCHEMA,
        handler=handle_source_select,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_fragment_verify",
        toolset="research",
        schema=FRAGMENT_VERIFY_SCHEMA,
        handler=handle_fragment_verify,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_claim_evaluate",
        toolset="research",
        schema=CLAIM_EVALUATE_SCHEMA,
        handler=handle_claim_evaluate,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_claim_verification_graph_assess",
        toolset="research",
        schema=CLAIM_VERIFICATION_GRAPH_SCHEMA,
        handler=handle_claim_verification_graph_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_numeric_reproduction_assess",
        toolset="research",
        schema=NUMERIC_REPRODUCTION_SCHEMA,
        handler=handle_numeric_reproduction_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_challenge_evaluate",
        toolset="research",
        schema=CHALLENGE_EVALUATE_SCHEMA,
        handler=handle_challenge_evaluate,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_synthesis_assess",
        toolset="research",
        schema=SYNTHESIS_ASSESS_SCHEMA,
        handler=handle_synthesis_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_evidence_standard_create",
        toolset="research",
        schema=EVIDENCE_STANDARD_CREATE_SCHEMA,
        handler=handle_evidence_standard_create,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_evidence_standard_propose_revision",
        toolset="research",
        schema=EVIDENCE_STANDARD_REVISE_SCHEMA,
        handler=handle_evidence_standard_revision,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_evidence_exception_assess",
        toolset="research",
        schema=EVIDENCE_EXCEPTION_ASSESS_SCHEMA,
        handler=handle_evidence_exception_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_claim_card_assess",
        toolset="research",
        schema=CLAIM_CARD_ASSESS_SCHEMA,
        handler=handle_claim_card_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_negative_knowledge_classify",
        toolset="research",
        schema=NEGATIVE_KNOWLEDGE_CLASSIFY_SCHEMA,
        handler=handle_negative_knowledge_classify,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_coverage_assess",
        toolset="research",
        schema=SEARCH_COVERAGE_ASSESS_SCHEMA,
        handler=handle_search_coverage_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_source_pool_audit",
        toolset="research",
        schema=SOURCE_POOL_AUDIT_SCHEMA,
        handler=handle_source_pool_audit,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_udr_architecture_select",
        toolset="research",
        schema=UDR_ARCHITECTURE_SELECT_SCHEMA,
        handler=handle_udr_architecture_select,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_udr_plan_assess",
        toolset="research",
        schema=UDR_PLAN_ASSESS_SCHEMA,
        handler=handle_udr_plan_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_quality_dashboard_project",
        toolset="research",
        schema=QUALITY_DASHBOARD_PROJECT_SCHEMA,
        handler=handle_quality_dashboard_project,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_decision_envelope_assess",
        toolset="research",
        schema=DECISION_ENVELOPE_ASSESS_SCHEMA,
        handler=handle_decision_envelope_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_delta_assess",
        toolset="research",
        schema=DELTA_ASSESS_SCHEMA,
        handler=handle_delta_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_incident_assess",
        toolset="research",
        schema=INCIDENT_ASSESS_SCHEMA,
        handler=handle_incident_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_independent_support_assess",
        toolset="research",
        schema=INDEPENDENT_SUPPORT_ASSESS_SCHEMA,
        handler=handle_independent_support_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_engagement_level_select",
        toolset="research",
        schema=ENGAGEMENT_LEVEL_SELECT_SCHEMA,
        handler=handle_engagement_level_select,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_engagement_level_propose_revision",
        toolset="research",
        schema=ENGAGEMENT_LEVEL_REVISE_SCHEMA,
        handler=handle_engagement_level_revision,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_parsing_result_assess",
        toolset="research",
        schema=PARSING_RESULT_ASSESS_SCHEMA,
        handler=handle_parsing_result_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_parse_intake_assess",
        toolset="research",
        schema=PARSE_INTAKE_ASSESS_SCHEMA,
        handler=handle_parse_intake_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_parse_runs_record",
        toolset="research",
        schema=PARSE_RUNS_RECORD_SCHEMA,
        handler=handle_parse_runs_record,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_unicode_representations_build",
        toolset="research",
        schema=UNICODE_REPRESENTATIONS_BUILD_SCHEMA,
        handler=handle_unicode_representations_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_document_graph_build",
        toolset="research",
        schema=DOCUMENT_GRAPH_BUILD_SCHEMA,
        handler=handle_document_graph_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_document_graph_verify",
        toolset="research",
        schema=DOCUMENT_GRAPH_VERIFY_SCHEMA,
        handler=handle_document_graph_verify,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_query_ast_compile",
        toolset="research",
        schema=QUERY_AST_COMPILE_SCHEMA,
        handler=handle_query_ast_compile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_strategy_assess",
        toolset="research",
        schema=SEARCH_STRATEGY_ASSESS_SCHEMA,
        handler=handle_search_strategy_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_environment_record",
        toolset="research",
        schema=SEARCH_ENVIRONMENT_RECORD_SCHEMA,
        handler=handle_search_environment_record,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_search_stop_assess",
        toolset="research",
        schema=SEARCH_STOP_ASSESS_SCHEMA,
        handler=handle_search_stop_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_screening_stop_assess",
        toolset="research",
        schema=SCREENING_STOP_ASSESS_SCHEMA,
        handler=handle_screening_stop_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_instrument_portfolio_build",
        toolset="research",
        schema=INSTRUMENT_PORTFOLIO_BUILD_SCHEMA,
        handler=handle_instrument_portfolio_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_instrument_strategy_build",
        toolset="research",
        schema=INSTRUMENT_STRATEGY_BUILD_SCHEMA,
        handler=handle_instrument_strategy_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_tool_query_build",
        toolset="research",
        schema=TOOL_QUERY_BUILD_SCHEMA,
        handler=handle_tool_query_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_instrument_strategy_propose_revision",
        toolset="research",
        schema=INSTRUMENT_STRATEGY_REVISE_SCHEMA,
        handler=handle_instrument_strategy_revision,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_brief_build",
        toolset="research",
        schema=BRIEF_BUILD_SCHEMA,
        handler=handle_brief_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_contextualization_build",
        toolset="research",
        schema=CONTEXTUALIZATION_BUILD_SCHEMA,
        handler=handle_contextualization_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_context_package_build",
        toolset="research",
        schema=CONTEXT_PACKAGE_BUILD_SCHEMA,
        handler=handle_context_package_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_debrief_assess",
        toolset="research",
        schema=DEBRIEF_ASSESS_SCHEMA,
        handler=handle_debrief_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_decomposition_assess",
        toolset="research",
        schema=DECOMPOSITION_ASSESS_SCHEMA,
        handler=handle_decomposition_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_construct_operationalize",
        toolset="research",
        schema=CONSTRUCT_OPERATIONALIZE_SCHEMA,
        handler=handle_construct_operationalize,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_construct_propose_revision",
        toolset="research",
        schema=CONSTRUCT_REVISE_SCHEMA,
        handler=handle_construct_revision,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_assurance_profile_assess",
        toolset="research",
        schema=ASSURANCE_PROFILE_ASSESS_SCHEMA,
        handler=handle_assurance_profile_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_basic_loop_assess",
        toolset="research",
        schema=BASIC_LOOP_ASSESS_SCHEMA,
        handler=handle_basic_loop_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_oversight_transitions_assess",
        toolset="research",
        schema=OVERSIGHT_TRANSITIONS_ASSESS_SCHEMA,
        handler=handle_oversight_transitions_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_role_profile_assess",
        toolset="research",
        schema=ROLE_PROFILE_ASSESS_SCHEMA,
        handler=handle_role_profile_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_role_independence_assess",
        toolset="research",
        schema=ROLE_INDEPENDENCE_ASSESS_SCHEMA,
        handler=handle_role_independence_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_consilium_plan_assess",
        toolset="research",
        schema=CONSILIUM_PLAN_ASSESS_SCHEMA,
        handler=handle_consilium_plan_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_consilium_result_assess",
        toolset="research",
        schema=CONSILIUM_RESULT_ASSESS_SCHEMA,
        handler=handle_consilium_result_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_topology_select",
        toolset="research",
        schema=TOPOLOGY_SELECT_SCHEMA,
        handler=handle_topology_select,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_modality_plan_assess",
        toolset="research",
        schema=MODALITY_PLAN_ASSESS_SCHEMA,
        handler=handle_modality_plan_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_fact_map_build",
        toolset="research",
        schema=FACT_MAP_BUILD_SCHEMA,
        handler=handle_fact_map_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_root_cause_map_build",
        toolset="research",
        schema=ROOT_CAUSE_MAP_BUILD_SCHEMA,
        handler=handle_root_cause_map_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_knowledge_projections_reconcile",
        toolset="research",
        schema=PROJECTIONS_RECONCILE_SCHEMA,
        handler=handle_knowledge_projections_reconcile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_narrative_plan_assess",
        toolset="research",
        schema=NARRATIVE_PLAN_ASSESS_SCHEMA,
        handler=handle_narrative_plan_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_attribution_assess",
        toolset="research",
        schema=ATTRIBUTION_ASSESS_SCHEMA,
        handler=handle_attribution_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_source_influence_assess",
        toolset="research",
        schema=SOURCE_INFLUENCE_ASSESS_SCHEMA,
        handler=handle_source_influence_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_narrative_diff_assess",
        toolset="research",
        schema=NARRATIVE_DIFF_ASSESS_SCHEMA,
        handler=handle_narrative_diff_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provenance_export_assess",
        toolset="research",
        schema=PROVENANCE_EXPORT_ASSESS_SCHEMA,
        handler=handle_provenance_export_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_replay_assess",
        toolset="research",
        schema=REPLAY_ASSESS_SCHEMA,
        handler=handle_replay_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_living_review_assess",
        toolset="research",
        schema=LIVING_REVIEW_ASSESS_SCHEMA,
        handler=handle_living_review_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_deep_qualification_assess",
        toolset="research",
        schema=DEEP_QUALIFICATION_ASSESS_SCHEMA,
        handler=handle_deep_qualification_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_obligation_preservation_assess",
        toolset="research",
        schema=OBLIGATION_PRESERVATION_ASSESS_SCHEMA,
        handler=handle_obligation_preservation_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_multiagent_independence_assess",
        toolset="research",
        schema=MULTIAGENT_INDEPENDENCE_ASSESS_SCHEMA,
        handler=handle_multiagent_independence_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_resilience_recovery_assess",
        toolset="research",
        schema=RESILIENCE_RECOVERY_ASSESS_SCHEMA,
        handler=handle_resilience_recovery_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_catalog_get",
        toolset="research",
        schema=PROVIDER_CATALOG_GET_SCHEMA,
        handler=handle_provider_catalog_get,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_manifest_build",
        toolset="research",
        schema=PROVIDER_MANIFEST_BUILD_SCHEMA,
        handler=handle_provider_manifest_build,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_schema_diff",
        toolset="research",
        schema=PROVIDER_SCHEMA_DIFF_SCHEMA,
        handler=handle_provider_schema_diff,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_operation_assess",
        toolset="research",
        schema=PROVIDER_OPERATION_ASSESS_SCHEMA,
        handler=handle_provider_operation_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_execution_assess",
        toolset="research",
        schema=PROVIDER_EXECUTION_ASSESS_SCHEMA,
        handler=handle_provider_execution_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_fallback_assess",
        toolset="research",
        schema=PROVIDER_FALLBACK_ASSESS_SCHEMA,
        handler=handle_provider_fallback_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_budget_reserve",
        toolset="research",
        schema=PROVIDER_BUDGET_RESERVE_SCHEMA,
        handler=handle_provider_budget_reserve,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_lifecycle_reconcile",
        toolset="research",
        schema=PROVIDER_LIFECYCLE_RECONCILE_SCHEMA,
        handler=handle_provider_lifecycle_reconcile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_receipt_normalize",
        toolset="research",
        schema=PROVIDER_RECEIPT_NORMALIZE_SCHEMA,
        handler=handle_provider_receipt_normalize,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_conformance_assess",
        toolset="research",
        schema=PROVIDER_CONFORMANCE_ASSESS_SCHEMA,
        handler=handle_provider_conformance_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_scholarly_object_resolve",
        toolset="research",
        schema=SCHOLARLY_OBJECT_RESOLVE_SCHEMA,
        handler=handle_scholarly_object_resolve,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_capability_gap_assess",
        toolset="research",
        schema=CAPABILITY_GAP_ASSESS_SCHEMA,
        handler=handle_capability_gap_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_business_design_assess",
        toolset="research",
        schema=BUSINESS_DESIGN_ASSESS_SCHEMA,
        handler=handle_business_design_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_business_control_assess",
        toolset="research",
        schema=BUSINESS_CONTROL_ASSESS_SCHEMA,
        handler=handle_business_control_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_academic_protocol_assess",
        toolset="research",
        schema=ACADEMIC_PROTOCOL_ASSESS_SCHEMA,
        handler=handle_academic_protocol_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_academic_integrity_assess",
        toolset="research",
        schema=ACADEMIC_INTEGRITY_ASSESS_SCHEMA,
        handler=handle_academic_integrity_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_meta_analysis_assess",
        toolset="research",
        schema=META_ANALYSIS_ASSESS_SCHEMA,
        handler=handle_meta_analysis_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_review_protocol_validate",
        toolset="research",
        schema=REVIEW_PROTOCOL_VALIDATE_SCHEMA,
        handler=handle_review_protocol_validate,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_screening_adjudicate",
        toolset="research",
        schema=SCREENING_ADJUDICATE_SCHEMA,
        handler=handle_screening_adjudicate,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_study_graph_resolve",
        toolset="research",
        schema=STUDY_GRAPH_RESOLVE_SCHEMA,
        handler=handle_study_graph_resolve,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_extraction_assess",
        toolset="research",
        schema=EXTRACTION_ASSESS_SCHEMA,
        handler=handle_extraction_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_prisma_assess",
        toolset="research",
        schema=PRISMA_ASSESS_SCHEMA,
        handler=handle_prisma_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_prisma_flow_account",
        toolset="research",
        schema=PRISMA_FLOW_ACCOUNT_SCHEMA,
        handler=handle_prisma_flow_account,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_risk_of_bias_assess",
        toolset="research",
        schema=RISK_OF_BIAS_ASSESS_SCHEMA,
        handler=handle_risk_of_bias_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_certainty_assess",
        toolset="research",
        schema=CERTAINTY_ASSESS_SCHEMA,
        handler=handle_certainty_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_academic_synthesis_gate",
        toolset="research",
        schema=ACADEMIC_SYNTHESIS_GATE_SCHEMA,
        handler=handle_academic_synthesis_gate,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_computation_replay_assess",
        toolset="research",
        schema=COMPUTATION_REPLAY_ASSESS_SCHEMA,
        handler=handle_computation_replay_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_fixed_effect_compute",
        toolset="research",
        schema=FIXED_EFFECT_COMPUTE_SCHEMA,
        handler=handle_fixed_effect_compute,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_review_assess",
        toolset="research",
        schema=REVIEW_ASSESS_SCHEMA,
        handler=handle_review_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_acceptance_assess",
        toolset="research",
        schema=ACCEPTANCE_ASSESS_SCHEMA,
        handler=handle_acceptance_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_release_assess",
        toolset="research",
        schema=RELEASE_ASSESS_SCHEMA,
        handler=handle_release_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_correction_assess",
        toolset="research",
        schema=CORRECTION_ASSESS_SCHEMA,
        handler=handle_correction_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_operation_reconcile",
        toolset="research",
        schema=OPERATION_RECONCILE_SCHEMA,
        handler=handle_operation_reconcile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_recovery_assess",
        toolset="research",
        schema=RECOVERY_ASSESS_SCHEMA,
        handler=handle_recovery_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_invalidation_assess",
        toolset="research",
        schema=INVALIDATION_ASSESS_SCHEMA,
        handler=handle_invalidation_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_object_revision_assess",
        toolset="research",
        schema=OBJECT_REVISION_ASSESS_SCHEMA,
        handler=handle_object_revision_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_context_assembly_assess",
        toolset="research",
        schema=CONTEXT_ASSEMBLY_ASSESS_SCHEMA,
        handler=handle_context_assembly_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_restore_assess",
        toolset="research",
        schema=RESTORE_ASSESS_SCHEMA,
        handler=handle_restore_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_bundle_import_assess",
        toolset="research",
        schema=BUNDLE_IMPORT_ASSESS_SCHEMA,
        handler=handle_bundle_import_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_legacy_migration_assess",
        toolset="research",
        schema=LEGACY_MIGRATION_ASSESS_SCHEMA,
        handler=handle_legacy_migration_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_deployment_candidate_assess",
        toolset="research",
        schema=DEPLOYMENT_CANDIDATE_SCHEMA,
        handler=handle_deployment_candidate_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_profile_qualification",
        toolset="research",
        schema=PROFILE_QUALIFICATION_SCHEMA,
        handler=handle_profile_qualification,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_depth_compare",
        toolset="research",
        schema=DEPTH_COMPARISON_SCHEMA,
        handler=handle_depth_compare,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_utility_assess",
        toolset="research",
        schema=UTILITY_ASSESS_SCHEMA,
        handler=handle_utility_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_greenfield_assess",
        toolset="research",
        schema=GREENFIELD_ASSESS_SCHEMA,
        handler=handle_greenfield_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_greenfield_accept",
        toolset="research",
        schema=GREENFIELD_ACCEPT_SCHEMA,
        handler=handle_greenfield_accept,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_foundation_assess",
        toolset="research",
        schema=FOUNDATION_ASSESS_SCHEMA,
        handler=handle_foundation_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_resource_admission_assess",
        toolset="research",
        schema=RESOURCE_ADMISSION_SCHEMA,
        handler=handle_resource_admission_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_migration_map_dry_run",
        toolset="research",
        schema=MIGRATION_MAP_SCHEMA,
        handler=handle_migration_map_dry_run,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_state_reconcile",
        toolset="research",
        schema=STATE_RECONCILE_SCHEMA,
        handler=handle_state_reconcile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_state_semantics_assess",
        toolset="research",
        schema=STATE_SEMANTICS_ASSESS_SCHEMA,
        handler=handle_state_semantics_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_security_control_assess",
        toolset="research",
        schema=SECURITY_CONTROL_ASSESS_SCHEMA,
        handler=handle_security_control_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_artifact_assess",
        toolset="research",
        schema=ARTIFACT_ASSESS_SCHEMA,
        handler=handle_artifact_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_fragment_promote",
        toolset="research",
        schema=FRAGMENT_PROMOTE_SCHEMA,
        handler=handle_fragment_promote,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_installation_assess",
        toolset="research",
        schema=INSTALLATION_ASSESS_SCHEMA,
        handler=handle_installation_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_context_lifecycle_assess",
        toolset="research",
        schema=CONTEXT_LIFECYCLE_SCHEMA,
        handler=handle_context_lifecycle_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_circuit_assess",
        toolset="research",
        schema=CIRCUIT_ASSESS_SCHEMA,
        handler=handle_circuit_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_dolt_commit_assess",
        toolset="research",
        schema=DOLT_COMMIT_ASSESS_SCHEMA,
        handler=handle_dolt_commit_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_capability_model_assess",
        toolset="research",
        schema=CAPABILITY_MODEL_SCHEMA,
        handler=handle_capability_model_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_provider_live_probe",
        toolset="research",
        schema=PROVIDER_LIVE_PROBE_SCHEMA,
        handler=handle_provider_live_probe,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_r3_evidence_assess",
        toolset="research",
        schema=R3_EVIDENCE_SCHEMA,
        handler=handle_r3_evidence_assess,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_context_package_assemble",
        toolset="research",
        schema=CONTEXT_ASSEMBLY_SCHEMA,
        handler=handle_context_package_assemble,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_work_liveness_reconcile",
        toolset="research",
        schema=LIVENESS_RECONCILE_SCHEMA,
        handler=handle_work_liveness_reconcile,
        check_fn=lambda: True,
    )
    ctx.register_tool(
        name="research_distribution_delivery_assess",
        toolset="research",
        schema=DISTRIBUTION_DELIVERY_SCHEMA,
        handler=handle_distribution_delivery_assess,
        check_fn=lambda: True,
    )
    ctx.register_skill(
        "research", Path(__file__).parent / "skills" / "research" / "SKILL.md"
    )
