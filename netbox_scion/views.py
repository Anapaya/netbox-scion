import csv
import io
import zipfile

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from netbox.views import generic
from . import forms, models, tables, filtersets


UTF8_BOM = b'\xef\xbb\xbf'


class UTF8BOMExportMixin:
    """Prepend a UTF-8 BOM to CSV exports so Excel handles encoding correctly."""

    def export_table(self, *args, **kwargs):
        response = super().export_table(*args, **kwargs)
        if hasattr(response, 'content'):
            response.content = UTF8_BOM + response.content
        return response


class PluginHomeView(UTF8BOMExportMixin, generic.ObjectListView):
    """Home view for the SCION plugin showing all main sections."""
    queryset = models.SCIONLink.objects.select_related('isd_as', 'isd_as__organization')
    table = tables.SCIONLinkTable
    filterset = filtersets.SCIONLinkFilterSet
    filterset_form = forms.SCIONLinkFilterForm
    template_name = 'generic/object_list.html'


def get_isdas_appliances(request):
    """AJAX view to get appliances for a specific ISD-AS"""
    isdas_id = request.GET.get('isdas_id')
    
    if isdas_id:
        try:
            isdas = models.ISDAS.objects.get(pk=isdas_id)
            appliances = isdas.appliances or []
            
            return JsonResponse({
                'appliances': appliances
            })
        except models.ISDAS.DoesNotExist:
            return JsonResponse({
                'error': 'ISD-AS not found',
                'appliances': []
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'appliances': []
            })
    
    return JsonResponse({
        'error': 'No ISD-AS ID provided',
        'appliances': []
    })


class OrganizationView(generic.ObjectView):
    queryset = models.Organization.objects.prefetch_related('isd_ases')
    template_name = 'netbox_scion/organization_detail.html'


class OrganizationListView(UTF8BOMExportMixin, generic.ObjectListView):
    queryset = models.Organization.objects.prefetch_related('isd_ases')
    table = tables.OrganizationTable
    filterset = filtersets.OrganizationFilterSet
    filterset_form = forms.OrganizationFilterForm


class OrganizationEditView(generic.ObjectEditView):
    queryset = models.Organization.objects.all()
    form = forms.OrganizationForm


class OrganizationDeleteView(generic.ObjectDeleteView):
    queryset = models.Organization.objects.all()


class OrganizationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Organization.objects.all()
    table = tables.OrganizationTable


class OrganizationChangeLogView(generic.ObjectChangeLogView):
    queryset = models.Organization.objects.all()
    model = models.Organization
    base_template = 'netbox_scion/organization_detail.html'


class ISDAView(generic.ObjectView):
    queryset = models.ISDAS.objects.select_related('organization')
    template_name = 'netbox_scion/isdas_detail.html'


class ISDAListView(UTF8BOMExportMixin, generic.ObjectListView):
    queryset = models.ISDAS.objects.select_related('organization').prefetch_related('links')
    table = tables.ISDATable
    filterset = filtersets.ISDAFilterSet
    filterset_form = forms.ISDAFilterForm


class ISDAEditView(generic.ObjectEditView):
    queryset = models.ISDAS.objects.all()
    form = forms.ISDAForm


class ISDADeleteView(generic.ObjectDeleteView):
    queryset = models.ISDAS.objects.all()


class ISDABulkDeleteView(generic.BulkDeleteView):
    queryset = models.ISDAS.objects.all()
    table = tables.ISDATable


class ISDAChangeLogView(generic.ObjectChangeLogView):
    queryset = models.ISDAS.objects.all()
    model = models.ISDAS
    base_template = 'netbox_scion/isdas_detail.html'


def add_appliance_to_isdas(request, pk):
    """Add an appliance to an ISD-AS"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    
    if request.method == 'POST':
        form = forms.ApplianceManagementForm(request.POST)
        if form.is_valid():
            appliance_name = form.cleaned_data['appliance_name']
            appliances = isdas.appliances or []
            
            if appliance_name not in appliances:
                appliances.append(appliance_name)
                isdas.appliances = appliances
                isdas.save()
                messages.success(request, f'Appliance "{appliance_name}" added successfully.')
            else:
                messages.error(request, f'Appliance "{appliance_name}" already exists.')
            
            return redirect('plugins:netbox_scion:isdas', pk=pk)
    else:
        form = forms.ApplianceManagementForm()
    
    return render(request, 'netbox_scion/add_core.html', {
        'form': form,
        'isdas': isdas,
        'return_url': request.GET.get('return_url', f"/plugins/scion/isdas/{pk}/"),
        'action': 'Add'
    })


def edit_appliance_in_isdas(request, pk, appliance_name):
    """Edit an appliance name in an ISD-AS"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    appliances = isdas.appliances or []
    
    if appliance_name not in appliances:
        messages.error(request, f'Appliance "{appliance_name}" not found.')
        return redirect('plugins:netbox_scion:isdas', pk=pk)
    
    if request.method == 'POST':
        form = forms.ApplianceManagementForm(request.POST)
        if form.is_valid():
            new_appliance_name = form.cleaned_data['appliance_name']
            
            if new_appliance_name != appliance_name:
                if new_appliance_name in appliances:
                    messages.error(request, f'Appliance "{new_appliance_name}" already exists.')
                else:
                    # Update appliance name in the list
                    appliance_index = appliances.index(appliance_name)
                    appliances[appliance_index] = new_appliance_name
                    isdas.appliances = appliances
                    isdas.save()
                    
                    # Update all SCION links that use this appliance
                    links = models.SCIONLink.objects.filter(
                        isd_as=isdas, core=appliance_name
                    )
                    links.update(core=new_appliance_name)
                    
                    messages.success(request, f'Appliance renamed from "{appliance_name}" to "{new_appliance_name}".')
            else:
                messages.info(request, 'No changes made.')
            
            return redirect('plugins:netbox_scion:isdas', pk=pk)
    else:
        form = forms.ApplianceManagementForm(initial={'appliance_name': appliance_name})
    
    return render(request, 'netbox_scion/add_core.html', {
        'form': form,
        'isdas': isdas,
        'return_url': request.GET.get('return_url', f"/plugins/scion/isdas/{pk}/"),
        'action': 'Edit',
        'appliance_name': appliance_name
    })


def remove_appliance_from_isdas(request, pk, appliance_name):
    """Remove an appliance from an ISD-AS and all associated SCION links"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    
    appliances = isdas.appliances or []
    if appliance_name in appliances:
        # Check how many SCION links will be deleted
        links_to_delete = models.SCIONLink.objects.filter(
            isd_as=isdas, core=appliance_name
        )
        links_count = links_to_delete.count()
        
        # Remove the appliance
        appliances.remove(appliance_name)
        isdas.appliances = appliances
        isdas.save()
        
        # Delete all associated SCION links
        if links_count > 0:
            links_to_delete.delete()
            messages.warning(
                request, 
                f'Appliance "{appliance_name}" removed successfully. '
                f'{links_count} SCION link(s) were also deleted.'
            )
        else:
            messages.success(request, f'Appliance "{appliance_name}" removed successfully.')
    else:
        messages.error(request, f'Appliance "{appliance_name}" not found.')
    
    return redirect('plugins:netbox_scion:isdas', pk=pk)


class SCIONLinkView(generic.ObjectView):
    queryset = models.SCIONLink.objects.select_related('isd_as', 'isd_as__organization')
    template_name = 'netbox_scion/scionlink_detail.html'


class SCIONLinkListView(UTF8BOMExportMixin, generic.ObjectListView):
    queryset = models.SCIONLink.objects.select_related('isd_as', 'isd_as__organization')
    table = tables.SCIONLinkTable
    filterset = filtersets.SCIONLinkFilterSet
    filterset_form = forms.SCIONLinkFilterForm


class SCIONLinkEditView(generic.ObjectEditView):
    queryset = models.SCIONLink.objects.all()
    form = forms.SCIONLinkForm
    template_name = 'netbox_scion/scionlink_edit.html'

    def get_extra_addanother_params(self, request):
        params = QueryDict(mutable=True)
        isd_as = request.POST.get('isd_as')
        if isd_as:
            params['isd_as'] = isd_as
        return params


class SCIONLinkDeleteView(generic.ObjectDeleteView):
    queryset = models.SCIONLink.objects.all()


class SCIONLinkBulkDeleteView(generic.BulkDeleteView):
    queryset = models.SCIONLink.objects.all()
    table = tables.SCIONLinkTable


class SCIONLinkChangeLogView(generic.ObjectChangeLogView):
    queryset = models.SCIONLink.objects.all()
    model = models.SCIONLink
    base_template = 'netbox_scion/scionlink_detail.html'


def _write_csv(buf, header, rows):
    """Write a CSV with UTF-8 BOM into *buf* (a text-mode or StringIO object)."""
    writer = csv.writer(buf)
    writer.writerow(header)
    writer.writerows(rows)


def export_organization(request, pk):
    """Export an organization and all related ISD-ASes / SCION Links as a ZIP of CSVs."""
    org = get_object_or_404(models.Organization, pk=pk)
    isd_ases = models.ISDAS.objects.filter(organization=org).order_by('isd_as')
    links = (
        models.SCIONLink.objects
        .filter(isd_as__organization=org)
        .select_related('isd_as')
        .order_by('isd_as__isd_as', 'interface_id')
    )

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # organization.csv
        org_csv = io.StringIO()
        _write_csv(org_csv, ['Short Name', 'Full Name', 'Description'], [
            [org.short_name, org.full_name, org.description],
        ])
        zf.writestr('organization.csv', UTF8_BOM.decode() + org_csv.getvalue())

        # isd_ases.csv
        isdas_csv = io.StringIO()
        _write_csv(
            isdas_csv,
            ['ISD-AS', 'Description', 'Appliances'],
            [[ia.isd_as, ia.description, ia.appliances_display] for ia in isd_ases],
        )
        zf.writestr('isd_ases.csv', UTF8_BOM.decode() + isdas_csv.getvalue())

        # scion_links.csv
        links_csv = io.StringIO()
        _write_csv(
            links_csv,
            [
                'ISD-AS', 'Appliance', 'Interface ID', 'Relationship', 'Status',
                'Peer Name', 'Peer', 'Local Underlay', 'Peer Underlay', 'Ticket',
            ],
            [
                [
                    lnk.isd_as.isd_as, lnk.core, lnk.interface_id, lnk.relationship,
                    lnk.status, lnk.peer_name, lnk.peer or '', lnk.local_underlay,
                    lnk.peer_underlay, lnk.ticket,
                ]
                for lnk in links
            ],
        )
        zf.writestr('scion_links.csv', UTF8_BOM.decode() + links_csv.getvalue())

    zip_buf.seek(0)
    filename = f'{org.short_name}_export.zip'
    response = HttpResponse(zip_buf.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
