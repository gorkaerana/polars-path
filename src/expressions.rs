use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::path::Path;

use polars_core::datatypes::{BooleanChunked};

pub fn wrap_path_exists(value: Option<&str>) -> Option<bool>{
    Some(value.map_or(false, |s| Path::new(s).exists()))
}

#[polars_expr(output_type=Boolean)]
fn exists(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: BooleanChunked = ca.apply_generic(wrap_path_exists);
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("exists only works on string data".into()))
    }
}
