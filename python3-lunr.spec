#
# Conditional build:
%bcond_without	doc		# API documentation
%bcond_without	tests		# unit+acceptance tests
%bcond_without	acctests	# acceptance tests

%define		module	lunr
Summary:	A Python implementation of Lunr.js
Summary(pl.UTF-8):	Pythonowa implementacja Lunr.js
Name:		python3-%{module}
Version:	0.8.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lunr/
Source0:	https://files.pythonhosted.org/packages/source/l/lunr/%{module}-%{version}.tar.gz
# Source0-md5:	ec394d06983ee22000d2c52d5892593c
URL:		https://pypi.org/project/lunr/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-fancy-pypi-readme >= 22.8.0
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
%if %{with acctests}
BuildRequires:	nodejs
%endif
BuildRequires:	python3-nltk
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-timeout
%if "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata
BuildRequires:	python3-typing_extensions
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-myst_parser
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This Python version of Lunr.js aims to bring the simple and powerful
full text search capabilities into Python guaranteeing results as
close as the original implementation as possible.

%description -l pl.UTF-8
Ta pythonowa wersja Lunr.js ma na celu dostarczenie prostej i mającej
duże możliwości funkcjonalności wyszukiwania pełnotekstowego do
Pythona, gwarantując efekty możliwie najbliższe oryginalnej
implementacji.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests %{!?with_acctests:-m 'not acceptance'}
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
